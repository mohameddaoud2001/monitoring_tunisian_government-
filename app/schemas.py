from marshmallow import Schema, fields, ValidationError
import re

def validate_governorate_code(code):
    if not re.match(r"^\d{2}$", code):
        raise ValidationError("Invalid governorate code format.")

def validate_delegation_code(code):
    if not re.match(r"^\d{4}$", code):
        raise ValidationError("Invalid delegation code format.")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role = fields.Str()
    jurisdiction = fields.Str()
    # Omit password for security

class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    name_ar = fields.Str()
    governorate = fields.Str()
    governorate_code = fields.Str(required=True, validate=validate_governorate_code)
    delegation_code = fields.Str(required=True, validate=validate_delegation_code)

class MinistrySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    name_ar = fields.Str()

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    project_code = fields.Str(required=False)
    title = fields.Str(required=True)
    title_ar = fields.Str()
    description = fields.Str()
    description_ar = fields.Str()
    budget = fields.Float()
    budget_currency = fields.Str(validate=lambda x: x in ['TND'])
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Str()
    region_id = fields.Int(required=True)
    ministry_id = fields.Int(required=True)

class DeliverableSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    title_ar = fields.Str()
    progress = fields.Float()
    project_id = fields.Int(required=True)  # Change this line

class FeedbackSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    content_ar = fields.Str()
    sentiment = fields.Float()
    project_id = fields.Int(required=True)  # Add this line
    user = fields.Nested(UserSchema, only=("id", "username"))

class ProjectStatsSchema(Schema):
    total_projects = fields.Int()
    projects_by_region = fields.List(fields.Nested(RegionSchema, only=("name", "governorate", "governorate_code", "delegation_code")), attribute="projects")
    projects_by_ministry = fields.List(fields.Nested(MinistrySchema, only=("name","name_ar")), attribute="projects")
    average_project_duration = fields.Float()
    budget_utilization = fields.Float()

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    description = fields.Str()
    date = fields.DateTime()
    project_id = fields.Int(required=True)

