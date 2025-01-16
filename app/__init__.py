import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_smorest import Api
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def create_app(config_name=None):
    load_dotenv()

    app = Flask(__name__, static_folder='../static')
    limiter.init_app(app)
    cache.init_app(app)

    # Load configuration based on the argument
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Config')

    # API metadata
    app.config.setdefault('API_TITLE', 'Tunisian Government Project Monitoring API')
    app.config.setdefault('API_VERSION', 'v1')
    app.config.setdefault('OPENAPI_VERSION', '3.0.3')
    app.config.setdefault('OPENAPI_URL_PREFIX', '/api/v1')
    app.config.setdefault('OPENAPI_SWAGGER_UI_PATH', '/swagger-ui')
    app.config.setdefault('OPENAPI_SWAGGER_UI_URL', 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Enable CORS for all routes

    # Initialize Flask-Smorest Api object
    api = Api(app)

    # Register blueprints
    from .routes.auth_routes import auth_blueprint
    from .routes.project_routes import project_blueprint
    from .routes.region_routes import region_blueprint
    from .routes.ministry_routes import ministry_blueprint
    from .routes.deliverable_routes import deliverable_blueprint
    from .routes.feedback_routes import feedback_blueprint
    from .routes.stats_routes import stats_blueprint
    from .routes.expense_routes import expense_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(project_blueprint, url_prefix='/api/v1/projects')
    app.register_blueprint(region_blueprint, url_prefix='/api/v1/regions')
    app.register_blueprint(ministry_blueprint, url_prefix='/api/v1/ministries')
    app.register_blueprint(deliverable_blueprint, url_prefix='/api/v1/deliverables')
    app.register_blueprint(feedback_blueprint, url_prefix='/api/v1/feedback')
    app.register_blueprint(stats_blueprint, url_prefix='/api/v1/stats')
    app.register_blueprint(expense_blueprint, url_prefix='/api/v1/expenses')

    # Serve static files correctly
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('../static', path)

    @app.route('/')
    def index():
        return send_from_directory('../static', 'index.html')

    # Error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found on this server.'}), 404

    # Error handler for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error has occurred on the server.'}), 500

    return app