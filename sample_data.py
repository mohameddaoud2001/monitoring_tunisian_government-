from app import create_app, db
from app.models import User, Region, Ministry, Project, Deliverable, Feedback, Expense
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

def create_sample_data():
    app = create_app()
    with app.app_context():
        try:
            # Don't drop existing data
            # db.drop_all() 
            db.create_all()

            # Create an admin user
            hashed_password = generate_password_hash('admin_password')
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', password=hashed_password, role='admin', jurisdiction='Central')
                db.session.add(admin)
                print("Admin user added.")

            # Create some regions
            region1 = Region.query.filter_by(name='Kairouan').first()
            if not region1:
                region1 = Region(name='Kairouan', name_ar='القيروان', governorate='Kairouan', governorate_code='31', delegation_code='3151')
                db.session.add(region1)
                print("Region Kairouan added.")

            region2 = Region.query.filter_by(name='Tunis').first()
            if not region2:
                region2 = Region(name='Tunis', name_ar='تونس', governorate='Tunis', governorate_code='11', delegation_code='1111')
                db.session.add(region2)
                print("Region Tunis added.")

            region3 = Region.query.filter_by(name='Sfax').first()
            if not region3:
                region3 = Region(name='Sfax', name_ar='صفاقس', governorate='Sfax', governorate_code='34', delegation_code='3451')
                db.session.add(region3)
                print("Region Sfax added.")

            # Create some ministries
            ministry1 = Ministry.query.filter_by(name='Ministry of Education').first()
            if not ministry1:
                ministry1 = Ministry(name='Ministry of Education', name_ar='وزارة التربية')
                db.session.add(ministry1)
                print("Ministry of Education added.")

            ministry2 = Ministry.query.filter_by(name='Ministry of Health').first()
            if not ministry2:
                ministry2 = Ministry(name='Ministry of Health', name_ar='وزارة الصحة')
                db.session.add(ministry2)
                print("Ministry of Health added.")

            ministry3 = Ministry.query.filter_by(name='Ministry of Infrastructure').first()
            if not ministry3:
                ministry3 = Ministry(name='Ministry of Infrastructure', name_ar='وزارة البنية التحتية')
                db.session.add(ministry3)
                print("Ministry of Infrastructure added.")

            db.session.commit()

            # Refresh to get IDs
            db.session.refresh(region1)
            db.session.refresh(region2)
            db.session.refresh(region3)
            db.session.refresh(ministry1)
            db.session.refresh(ministry2)
            db.session.refresh(ministry3)

            # Create some projects
            project1 = Project.query.filter_by(project_code='EDU-KAI-2024-01').first()
            if not project1:
                project1 = Project(
                    project_code='EDU-KAI-2024-01',
                    title='Construction of a new school in Kairouan',
                    title_ar='بناء مدرسة جديدة في القيروان',
                    description='This project aims to build a new elementary school in the Kairouan region.',
                    description_ar='يهدف هذا المشروع إلى بناء مدرسة ابتدائية جديدة في منطقة القيروان.',
                    budget=500000.00,
                    budget_currency='TND',
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=365),
                    status='In Progress',
                    region_id=region1.id,
                    ministry_id=ministry1.id
                )
                db.session.add(project1)
                print("Project 1 added.")

            project2 = Project.query.filter_by(project_code='HEA-TUN-2024-01').first()
            if not project2:
                project2 = Project(
                    project_code='HEA-TUN-2024-01',
                    title='Renovation of a hospital in Tunis',
                    title_ar='تجديد مستشفى في تونس',
                    description='This project involves renovating an existing hospital in Tunis.',
                    description_ar='يتضمن هذا المشروع تجديد مستشفى قائم في تونس.',
                    budget=800000.00,
                    budget_currency='TND',
                    start_date=datetime.now() - timedelta(days=60),
                    end_date=datetime.now() + timedelta(days=180),
                    status='In Progress',
                    region_id=region2.id,
                    ministry_id=ministry2.id
                )
                db.session.add(project2)
                print("Project 2 added.")

            project3 = Project.query.filter_by(project_code='INF-SFA-2024-01').first()
            if not project3:
                project3 = Project(
                    project_code='INF-SFA-2024-01',
                    title='Construction of a new bridge in Sfax',
                    title_ar='بناء جسر جديد في صفاقس',
                    description='This project aims to build a new bridge to improve traffic flow in Sfax.',
                    description_ar='يهدف هذا المشروع إلى بناء جسر جديد لتحسين تدفق حركة المرور في صفاقس.',
                    budget=1200000.00,
                    budget_currency='TND',
                    start_date=datetime.now() - timedelta(days=120),
                    end_date=datetime.now() + timedelta(days=240),
                    status='Delayed',
                    region_id=region3.id,
                    ministry_id=ministry3.id
                )
                db.session.add(project3)
                print("Project 3 added.")

            db.session.commit()

            # Refresh to get project IDs
            db.session.refresh(project1)
            db.session.refresh(project2)
            db.session.refresh(project3)

            # Create some deliverables for project1
            deliverable1 = Deliverable.query.filter_by(title='Site Preparation', project_id=project1.id).first()
            if not deliverable1:
                deliverable1 = Deliverable(title='Site Preparation', title_ar='تجهيز الموقع', progress=100.0, project_id=project1.id)
                db.session.add(deliverable1)
                print("Deliverable 1 added.")

            deliverable2 = Deliverable.query.filter_by(title='Foundation Laying', project_id=project1.id).first()
            if not deliverable2:
                deliverable2 = Deliverable(title='Foundation Laying', title_ar='وضع الأساس', progress=80.0, project_id=project1.id)
                db.session.add(deliverable2)
                print("Deliverable 2 added.")

            deliverable3 = Deliverable.query.filter_by(title='Wall Construction', project_id=project1.id).first()
            if not deliverable3:
                deliverable3 = Deliverable(title='Wall Construction', title_ar='بناء الجدران', progress=50.0, project_id=project1.id)
                db.session.add(deliverable3)
                print("Deliverable 3 added.")

            # Create some feedback entries for project1
            feedback1 = Feedback.query.filter_by(content='The project is progressing well.', project_id=project1.id).first()
            if not feedback1:
                feedback1 = Feedback(content='The project is progressing well.', content_ar='المشروع يتقدم بشكل جيد.', sentiment=0.5, project_id=project1.id, user_id=admin.id)
                db.session.add(feedback1)
                print("Feedback 1 added.")

            feedback2 = Feedback.query.filter_by(content='There have been some delays, but overall it is satisfactory.', project_id=project1.id).first()
            if not feedback2:
                feedback2 = Feedback(content='There have been some delays, but overall it is satisfactory.', content_ar='كانت هناك بعض التأخيرات، لكن بشكل عام الوضع مرضي.', sentiment=0.2, project_id=project1.id, user_id=admin.id)
                db.session.add(feedback2)
                print("Feedback 2 added.")

            # Create some expenses for project1
            expense1 = Expense.query.filter_by(description='Purchase of construction materials', project_id=project1.id).first()
            if not expense1:
                expense1 = Expense(amount=50000.00, description='Purchase of construction materials', date=datetime.now() - timedelta(days=30), project_id=project1.id)
                db.session.add(expense1)
                print("Expense 1 added.")

            expense2 = Expense.query.filter_by(description='Labor costs', project_id=project1.id).first()
            if not expense2:
                expense2 = Expense(amount=20000.00, description='Labor costs', date=datetime.now() - timedelta(days=15), project_id=project1.id)
                db.session.add(expense2)
                print("Expense 2 added.")

            db.session.commit()
            print("Sample data created successfully!")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

        except Exception as e:
            db.session.rollback()
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    create_sample_data()
