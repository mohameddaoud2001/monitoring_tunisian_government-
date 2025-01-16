from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Feedback, User, db
from app.schemas import FeedbackSchema
from app.utils import analyze_sentiment
from flask_smorest import Blueprint, abort

feedback_blueprint = Blueprint('feedback', __name__, url_prefix='/feedback')
feedback_schema = FeedbackSchema()

@feedback_blueprint.route('/', methods=['POST'])
@jwt_required()
@feedback_blueprint.arguments(FeedbackSchema)
@feedback_blueprint.response(201, FeedbackSchema)
def create_feedback(data):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        abort(404, message="User not found")

    # Analyze sentiment if content is provided
    if 'content' in data:
        sentiment = analyze_sentiment(data['content'])
    else:
        sentiment = None

    new_feedback = Feedback(
        content=data.get('content'),
        content_ar=data.get('content_ar'),
        sentiment=sentiment,
        project_id=data.get('project_id'),
        user_id=current_user_id
    )
    db.session.add(new_feedback)
    db.session.commit()
    return new_feedback

@feedback_blueprint.route('/', methods=['GET'])
@jwt_required()
@feedback_blueprint.response(200, FeedbackSchema(many=True))
def get_feedback():
    feedback = Feedback.query.all()
    return feedback

@feedback_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback deleted successfully'}), 200

