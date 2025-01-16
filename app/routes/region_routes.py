from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Region
from app.schemas import RegionSchema

region_blueprint = Blueprint('region', __name__, url_prefix='/regions')

region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)

@region_blueprint.route('/', methods=['GET'], strict_slashes=False)
def get_regions():
    all_regions = Region.query.all()
    result = regions_schema.dump(all_regions)
    return jsonify(result)

@region_blueprint.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_region():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = region_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    existing_region = Region.query.filter_by(name=data['name'], governorate_code=data['governorate_code']).first()
    if existing_region:
        return jsonify({'message': 'Region already exists'}), 409

    region = Region(
        name=data['name'],
        name_ar=data.get('name_ar'),
        governorate=data['governorate'],
        governorate_code=data['governorate_code'],
        delegation_code=data['delegation_code']
    )

    db.session.add(region)
    db.session.commit()

    result = region_schema.dump(region)
    return jsonify(result), 201
