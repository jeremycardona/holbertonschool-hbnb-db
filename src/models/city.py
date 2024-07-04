"""
City related functionality
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src import db  # Assuming `db` is your SQLAlchemy instance
from src.models.country import Country


class City(db.Model):
    """City representation"""

    __tablename__ = 'city'

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    country_code = Column(String(10), ForeignKey('country.code'), nullable=False)

    country = relationship("Country", back_populates="cities")

    def __init__(self, name: str, country_code: str, **kw) -> None:
        """Initializer for the City class"""
        super().__init__(**kw)
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """String representation of City object"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        from src.persistence import repo

        country = Country.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        new_city = City(name=data["name"], country_code=data["country_code"])

        repo.save(new_city)

        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City | None":
        """Update an existing city"""
        from src.persistence import repo

        city = City.query.get(city_id)

        if not city:
            return None

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city

    @classmethod
    def get_all(cls):
        """Retrieve all cities"""
        return cls.query.all()