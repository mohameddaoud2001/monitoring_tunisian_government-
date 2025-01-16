from app.models import Project, Region, Ministry
from app.schemas import ProjectSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.errors import ProjectNotFoundError

class ProjectService:
    def __init__(self, db):
        self.db = db

    def create_project(self, data):
        """Creates a new project."""
        region_id = data.get('region_id')
        ministry_id = data.get('ministry_id')

        # Validate region and ministry existence using db.session
        if not self.db.session.get(Region, region_id):
            raise ValueError(f"Region with ID {region_id} not found.")
        if not self.db.session.get(Ministry, ministry_id):
            raise ValueError(f"Ministry with ID {ministry_id} not found.")

        project = Project(**data)
        self.db.session.add(project)
        try:
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            if "project_code" in str(e):
                raise ValueError("A project with that code already exists.") from e
            else:
                raise ValueError("An error occurred while creating the project.") from e
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise ValueError("An unexpected database error occurred.") from e

        return project

    def get_projects(self, filters=None, sort_by='id', sort_order='asc', page=1, per_page=10):
        """Retrieves a list of projects with optional filtering, sorting, and pagination."""
        query = self.db.session.query(Project).options(
            joinedload(Project.region),
            joinedload(Project.ministry)
        )

        if filters:
            if filters.get('region'):
                query = query.filter(Project.region.has(name=filters['region']))
            if filters.get('status'):
                query = query.filter(Project.status == filters['status'])
            if filters.get('governorate_code'):
                query = query.filter(Project.region.has(governorate_code=filters['governorate_code']))
            if filters.get('ministry_id'):
                query = query.filter(Project.ministry_id == filters['ministry_id'])

        if sort_order == 'asc':
            query = query.order_by(getattr(Project, sort_by).asc())
        else:
            query = query.order_by(getattr(Project, sort_by).desc())

        projects = query.paginate(page=page, per_page=per_page, error_out=False)
        return projects

    def get_project_by_id(self, project_id):
        """Retrieves a project by its ID using db.session."""
        project = self.db.session.get(
            Project,
            project_id,
            options=[joinedload(Project.region), joinedload(Project.ministry)]
        )
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        return project