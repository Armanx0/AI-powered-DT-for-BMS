"""Role-based access control"""

from enum import Enum
from typing import List


class Role(str, Enum):
    """User roles"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class Permission:
    """Permission definitions"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


def check_permission(user_role: Role, required_permission: str) -> bool:
    """Check if user role has required permission"""
    permissions = {
        Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
        Role.USER: [Permission.READ, Permission.WRITE],
        Role.VIEWER: [Permission.READ],
    }
    return required_permission in permissions.get(user_role, [])
