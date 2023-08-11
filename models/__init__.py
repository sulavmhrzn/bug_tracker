from .bugs import Bug
from .projects import Project
from .users import User


def gather_models():
    return [User, Project, Bug]
