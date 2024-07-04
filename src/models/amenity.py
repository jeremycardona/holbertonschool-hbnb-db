"""
Amenity related functionality
"""

# src/models/amenity.py

from sqlalchemy import Column, String
from src import db  # Assuming `db` is your SQLAlchemy instance

class Amenity(db.Model):
    """Amenity representation"""

    __tablename__ = 'amenity'

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)

    def __init__(self, name: str, **kwargs) -> None:
        """Initializer for the Amenity class"""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self) -> str:
        """String representation of Amenity object"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        from src.persistence import repo

        amenity = Amenity(**data)

        repo.save(amenity)

        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        from src.persistence import repo

        amenity = Amenity.query.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        repo.update(amenity)

        return amenity

    @classmethod
    def get_all(cls):
        """Retrieve all amenities"""
        return cls.query.all()