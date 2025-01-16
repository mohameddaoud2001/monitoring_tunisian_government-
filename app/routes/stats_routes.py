from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Project, Region, Ministry, Feedback
from sqlalchemy import func
from statistics import mean

stats_blueprint = Blueprint('stats', __name__, url_prefix='/stats')

@stats_blueprint.route('/projects', methods=['GET'])
@jwt_required()
def project_stats():
    total_projects = Project.query.count()

    projects_by_region = []
    for region, count in db.session.query(Region, func.count(Project.id).label('count')) \
            .outerjoin(Project, Region.id == Project.region_id) \
            .group_by(Region) \
            .all():
        projects_by_region.append({
            'region_name': region.name,
            'region_name_ar': region.name_ar,
            'governorate': region.governorate,
            'governorate_code': region.governorate_code,
            'delegation_code': region.delegation_code,
            'project_count': count
        })

    projects_by_ministry = []
    for ministry, count in db.session.query(Ministry, func.count(Project.id).label('count')) \
            .outerjoin(Project, Ministry.id == Project.ministry_id) \
            .group_by(Ministry) \
            .all():
        projects_by_ministry.append({
            'ministry_name': ministry.name,
            'ministry_name_ar': ministry.name_ar,
            'project_count': count
        })

    completed_projects = Project.query.filter(Project.status == 'Completed').all()
    durations = [(project.end_date - project.start_date).days for project in completed_projects if project.end_date and project.start_date]
    average_duration = mean(durations) if durations else 0

    total_budget_allocated = db.session.query(func.sum(Project.budget)).scalar() or 0

    stats = {
        'total_projects': total_projects,
        'projects_by_region': projects_by_region,
        'projects_by_ministry': projects_by_ministry,
        'average_project_duration': average_duration,
        'budget_utilization': 0,  # Replace with calculated value (TODO)
    }

    return jsonify(stats)

@stats_blueprint.route('/feedback', methods=['GET'])
@jwt_required()
def feedback_stats():
    average_sentiment = db.session.query(func.avg(Feedback.sentiment)).scalar() or 0

    positive_count = Feedback.query.filter(Feedback.sentiment >= 0.5).count()
    negative_count = Feedback.query.filter(Feedback.sentiment <= -0.5).count()
    neutral_count = Feedback.query.filter(Feedback.sentiment > -0.5, Feedback.sentiment < 0.5).count()

    return jsonify({
        'average_sentiment': average_sentiment,
        'positive_feedback_count': positive_count,
        'negative_feedback_count': negative_count,
        'neutral_feedback_count': neutral_count,
    })
