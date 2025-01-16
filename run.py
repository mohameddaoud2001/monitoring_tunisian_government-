from app import create_app, db
from app.models import User  # Import User model
from werkzeug.security import generate_password_hash

app = create_app()

def create_initial_users():
    with app.app_context():
        # Create an admin user if not exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            hashed_password = generate_password_hash('admin_password')
            admin = User(username='admin', password=hashed_password, role='admin', jurisdiction='Central')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the tables
        create_initial_users()  # Create admin user if not exists

    app.run(debug=True)
