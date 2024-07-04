"""
Place related functionality
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src import db  # Assuming `db` is your SQLAlchemy instance

class Place(db.Model):
    """Place representation"""

    __tablename__ = 'place'

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    city_id = Column(String(36), ForeignKey('city.id'), nullable=False)
    price_per_night = Column(Integer, nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    max_guests = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    host = relationship('User', backref='places')
    city = relationship('City', backref='places')

    def __repr__(self) -> str:
        """String representation of Place object"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "host_id": self.host_id,
            "city_id": self.city_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        from src.models.user import User
        from src.models.city import City
        from src import db

        user = User.query.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city = City.query.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(**data)
        db.session.add(new_place)
        db.session.commit()

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place":
        """Update an existing place"""
        from src.models.user import User
        from src.models.city import City
        from src import db

        place = Place.query.get(place_id)
        if not place:
            raise ValueError("Place not found")

        user = User.query.get(data.get("host_id"))
        if user:
            place.host_id = user.id

        city = City.query.get(data.get("city_id"))
        if city:
            place.city_id = city.id

        place.name = data.get("name", place.name)
        place.description = data.get("description", place.description)
        place.address = data.get("address", place.address)
        place.latitude = data.get("latitude", place.latitude)
        place.longitude = data.get("longitude", place.longitude)
        place.price_per_night = data.get("price_per_night", place.price_per_night)
        place.number_of_rooms = data.get("number_of_rooms", place.number_of_rooms)
        place.number_of_bathrooms = data.get("number_of_bathrooms", place.number_of_bathrooms)
        place.max_guests = data.get("max_guests", place.max_guests)
        place.updated_at = datetime.utcnow()

        db.session.commit()

        return place
    
    @classmethod
    def get_all(cls):
        """Retrieve all places"""
        return cls.query.all()