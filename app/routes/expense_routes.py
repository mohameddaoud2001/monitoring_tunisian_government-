from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Expense, db
from app.schemas import ExpenseSchema
from flask_smorest import Blueprint, abort

expense_blueprint = Blueprint('expenses', __name__, url_prefix='/expenses')
expense_schema = ExpenseSchema()

@expense_blueprint.route('/', methods=['POST'])
@jwt_required()
@expense_blueprint.arguments(ExpenseSchema)
@expense_blueprint.response(201, ExpenseSchema)
def create_expense(data):
    new_expense = Expense(**data)
    db.session.add(new_expense)
    db.session.commit()
    return new_expense

@expense_blueprint.route('/', methods=['GET'])
@jwt_required()
@expense_blueprint.response(200, ExpenseSchema(many=True))
def get_expenses():
    expenses = Expense.query.all()
    return expenses

@expense_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
@expense_blueprint.arguments(ExpenseSchema)
@expense_blueprint.response(200, ExpenseSchema)
def update_expense(data, id):
    expense = Expense.query.get_or_404(id)
    for key, value in data.items():
        setattr(expense, key, value)
    db.session.commit()
    return expense

@expense_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'}), 200