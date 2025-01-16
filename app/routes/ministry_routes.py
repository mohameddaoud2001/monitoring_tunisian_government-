from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Ministry
from app.schemas import MinistrySchema

ministry_blueprint = Blueprint('ministry', __name__, url_prefix='/ministries')

ministry_schema = MinistrySchema()
ministries_schema = MinistrySchema(many=True)

@ministry_blueprint.route('/', methods=['GET'], strict_slashes=False)
def get_ministries():
    all_ministries = Ministry.query.all()
    result = ministries_schema.dump(all_ministries)
    return jsonify(result)

@ministry_blueprint.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_ministry():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = ministry_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    existing_ministry = Ministry.query.filter_by(name=data['name']).first()
    if existing_ministry:
        return jsonify({'message': 'Ministry already exists'}), 409

    ministry = Ministry(
        name=data['name'],
        name_ar=data.get('name_ar')
    )

    db.session.add(ministry)
    db.session.commit()

    result = ministry_schema.dump(ministry)
    return jsonify(result), 201
