from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src import db 
from src.models.base import Base


class PlaceAmenity(db.Model):
    """PlaceAmenity representation"""

    __tablename__ = 'placeamenity'

    id = Column(String(36), primary_key=True)
    place_id = Column(String(36), ForeignKey('place.id'), nullable=False)
    amenity_id = Column(String(36), ForeignKey('amenity.id'), nullable=False)

    place = relationship("Place", back_populates="place_amenities")
    amenity = relationship("Amenity", back_populates="place_amenities")

    def __init__(self, place_id: str, amenity_id: str, **kw) -> None:
        """Initializer for the PlaceAmenity class"""
        super().__init__(**kw)
        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """String representation of PlaceAmenity object"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.query.filter_by(place_id=place_id, amenity_id=amenity_id).first()

        return place_amenity

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        from src.persistence import repo

        new_place_amenity = PlaceAmenity(**data)

        repo.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        repo.delete(place_amenity)

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
