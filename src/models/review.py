from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src import db  # Assuming `db` is your SQLAlchemy instance

class Review(db.Model):
    """Review representation"""

    __tablename__ = 'review'

    id = Column(String(36), primary_key=True)
    place_id = Column(String(36), ForeignKey('place.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    comment = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship('Place', backref='reviews')
    user = relationship('User', backref='reviews')

    def __repr__(self) -> str:
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        from src.models.user import User
        from src.models.place import Place
        from src import db

        user = User.query.get(data["user_id"])
        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = Place.query.get(data["place_id"])
        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        db.session.add(new_review)
        db.session.commit()

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review":
        """Update an existing review"""
        from src.models.user import User
        from src.models.place import Place
        from src import db

        review = Review.query.get(review_id)
        if not review:
            raise ValueError("Review not found")

        user = User.query.get(data.get("user_id"))
        if user:
            review.user_id = user.id

        place = Place.query.get(data.get("place_id"))
        if place:
            review.place_id = place.id

        review.comment = data.get("comment", review.comment)
        review.rating = data.get("rating", review.rating)
        review.updated_at = datetime.utcnow()

        db.session.commit()

        return review

    @classmethod
    def get_all(cls):
        return cls.query.all()