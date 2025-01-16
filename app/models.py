from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50))  # 'admin', 'ministry_user', 'region_user', 'citizen'
    jurisdiction = db.Column(db.String(100))  # e.g., 'Ministry of Education', 'Kairouan'

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    name_ar = db.Column(db.String(80)) # Arabic name
    governorate = db.Column(db.String(80))
    governorate_code = db.Column(db.String(2), index=True)
    delegation_code = db.Column(db.String(4))
    projects = db.relationship('Project', backref='region', lazy=True)

class Ministry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False) # e.g., "Ministry of Education"
    name_ar = db.Column(db.String(120)) # Arabic name
    projects = db.relationship('Project', backref='ministry', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String, unique=True, nullable=True)
    title = db.Column(db.String(120), nullable=False)
    title_ar = db.Column(db.String(120))  # Arabic title
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)    # Arabic description
    budget = db.Column(db.Float)
    budget_currency = db.Column(db.String(3), default="TND") # Tunisian Dinar
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), index=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False, index=True)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.id'), nullable=False, index=True)
    deliverables = db.relationship('Deliverable', backref='project', lazy=True)
    expenses = db.relationship('Expense', backref='project', lazy=True)

class Deliverable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    title_ar = db.Column(db.String(120)) # Arabic title
    progress = db.Column(db.Float, default=0.0)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    content_ar = db.Column(db.String(500))  # Arabic content (optional)
    sentiment = db.Column(db.Float)  # Sentiment score (-1 to 1)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
