"""
User related functionality
"""

from src import bcrypt, db
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime


class User(db.Model):
    """User representation"""
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Ensure secure storage
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, email: str, first_name: str, last_name: str, password: str, **kw):
        """Initialize a new User object"""
        super().__init__(**kw)
        self.id = str(uuid.uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)

    def set_password(self, password: str):
        """Hash and set the user's password"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check the user's password against the stored hash"""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self) -> str:
        """Return a string representation of the User object"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Return a dictionary representation of the User object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create(user_data: dict) -> "User":
        """Create a new user in the database"""
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user in the database"""
        user = User.query.get(user_id)
        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.set_password(data["password"])
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "is_admin" in data:
            user.is_admin = data["is_admin"]

        db.session.commit()
        return user

    @staticmethod
    def get(user_id: str) -> "User | None":
        """Retrieve a user by ID from the database"""
        return User.query.get(user_id)

    @staticmethod
    def get_all() -> list["User"]:
        """Retrieve all users from the database"""
        return db.session.query(User).all()
