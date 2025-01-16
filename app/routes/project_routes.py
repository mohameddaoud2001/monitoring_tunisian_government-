from flask import Blueprint, request, jsonify, url_for, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import func  # Import func
from app import db, cache
from app.models import Project, Region, Ministry
from app.schemas import ProjectSchema
from app.services import ProjectService
from app.errors import ProjectNotFoundError, DuplicateProjectError

project_blueprint = Blueprint('project', __name__, url_prefix='/projects')

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

# Initialize ProjectService
project_service = ProjectService(db)

@project_blueprint.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_project():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = project_schema.load(json_data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 422

    try:
        project = project_service.create_project(data)
        result = project_schema.dump(project)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@project_blueprint.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def get_projects():
    try:
        current_user = get_jwt_identity()
        print(f"Current user accessing projects: {current_user}")

        # Get the JWT claims (for authorization logic)
        claims = get_jwt()
        user_role = claims.get("role")
        user_jurisdiction = claims.get("jurisdiction")

        print(f"User role: {user_role}, User jurisdiction: {user_jurisdiction}")

        filters = {
            'region': request.args.get('region'),
            'status': request.args.get('status'),
            'governorate_code': request.args.get('governorate_code'),
            'ministry_id': request.args.get('ministry_id')
        }

        # Authorization filters (uncomment and adapt as needed)
        # if user_role == 'ministry_user':
        #     ministry = Ministry.query.filter_by(name=user_jurisdiction).first()
        #     if not ministry:
        #         abort(403, message="You do not have permission to access projects for this ministry.")
        #     filters['ministry_id'] = ministry.id
        # elif user_role == 'region_user':
        #     region = Region.query.filter_by(name=user_jurisdiction).first()
        #     if not region:
        #         abort(403, message="You do not have permission to access projects for this region.")
        #     filters['region'] = region.name

        sort_by = request.args.get('sort_by', 'id')
        sort_order = request.args.get('sort_order', 'asc')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        projects = project_service.get_projects(filters, sort_by, sort_order, page, per_page)
        project_items = projects.items

        print(f"Projects query: {project_items}")

        result = projects_schema.dump(project_items)
        print(f"Number of projects fetched: {len(result)}")
        print(f"Projects data: {result}")

        return jsonify({
            'data': result,
            'page': projects.page,
            'total_pages': projects.pages,
            'total_items': projects.total
        })

    except Exception as e:
        print(f"Error fetching projects: {e}")
        return jsonify({'error': str(e)}), 500

@project_blueprint.route('/debug', methods=['GET'])
def debug_projects():
    projects = Project.query.all()
    regions = Region.query.all()
    ministries = Ministry.query.all()

    return jsonify({
        'project_count': len(projects),
        'region_count': len(regions),
        'ministry_count': len(ministries),
        'first_project': project_schema.dump(projects[0]) if projects else None,
        'projects': projects_schema.dump(projects)  # Return all projects for debugging
    })

@project_blueprint.route('/search', methods=['GET'])
def search_projects():
    search_term = request.args.get('q')

    if not search_term:
        return jsonify({'message': 'No search term provided'}), 400

    search_pattern = f"%{search_term}%"
    query = Project.query.filter(
        (Project.title.ilike(search_pattern)) |
        (Project.description.ilike(search_pattern))
    )

    projects = query.all()
    result = projects_schema.dump(projects)
    return jsonify(result)

@project_blueprint.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = project_service.get_project_by_id(project_id)
        result = project_schema.dump(project)

        result['_links'] = {
            'self': url_for('project.get_project', project_id=project_id, _external=True),
            'update': url_for('project.update_project', project_id=project_id, _external=True),
            'delete': url_for('project.delete_project', project_id=project_id, _external=True),
            'deliverables': url_for('deliverables.get_deliverables', project_id=project_id, _external=True)
        }

        return jsonify(result)
    except ProjectNotFoundError as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred'}), 500

@project_blueprint.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = project_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(project, key, value)

    db.session.commit
    return project_schema.dump(project)


@project_blueprint.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    return jsonify({'message': 'Project deleted successfully'})

