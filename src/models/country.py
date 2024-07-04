"""
Country related functionality
"""
from sqlalchemy import Column, String, Integer
from src import db  # Assuming `db` is your SQLAlchemy instance

class Country(db.Model):
    """
    Country representation
    
    This class inherits from db.Model, allowing for full CRUD operations
    """

    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    cities = db.relationship('City', back_populates='country', lazy=True)
    
    def __init__(self, name: str, code: str, **kw) -> None:
        """Initializer for the Country class"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """String representation of Country object"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        return Country.query.all()

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        return Country.query.filter_by(code=code).first()

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        new_country = Country(name=name, code=code)
        db.session.add(new_country)
        db.session.commit()
        return new_country

