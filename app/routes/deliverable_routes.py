from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Deliverable, db
from app.schemas import DeliverableSchema
from flask_smorest import Blueprint, abort

deliverable_blueprint = Blueprint('deliverables', __name__, url_prefix='/deliverables')
deliverable_schema = DeliverableSchema()

@deliverable_blueprint.route('/', methods=['POST'])
@jwt_required()
@deliverable_blueprint.arguments(DeliverableSchema)
@deliverable_blueprint.response(201, DeliverableSchema)
def create_deliverable(data):
    new_deliverable = Deliverable(**data)
    db.session.add(new_deliverable)
    db.session.commit()
    return new_deliverable

@deliverable_blueprint.route('/', methods=['GET'])
@jwt_required()
@deliverable_blueprint.response(200, DeliverableSchema(many=True))
def get_deliverables():
    deliverables = Deliverable.query.all()
    return deliverables

@deliverable_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
@deliverable_blueprint.arguments(DeliverableSchema)
@deliverable_blueprint.response(200, DeliverableSchema)
def update_deliverable(data, id):
    deliverable = Deliverable.query.get_or_404(id)
    for key, value in data.items():
        setattr(deliverable, key, value)
    db.session.commit()
    return deliverable

@deliverable_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_deliverable(id):
    deliverable = Deliverable.query.get_or_404(id)
    db.session.delete(deliverable)
    db.session.commit()
    return jsonify({'message': 'Deliverable deleted successfully'}), 200

