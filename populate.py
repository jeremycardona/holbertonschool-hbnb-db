from src.models.user import User
from src.models.country import Country
from src.models.city import City
from src.models.place import Place
from src import create_app, db

app = create_app()
def populate_users():
    sample_users = [
        {
            "email": "user12@example.com",
            "first_name": "Bob",
            "last_name": "Craig",
            "password": "password1"
        },
        {
            "email": "user22@example.com",
            "first_name": "Jenny",
            "last_name": "Craig",
            "password": "password2"
        },
        {
            "email": "user33@example.com",
            "first_name": "Will",
            "last_name": "Craig",
            "password": "password3"
        }
    ]

    with app.app_context():
        for user_data in sample_users:
            user = User(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                password=user_data["password"]
            )
            db.session.add(user)
        db.session.commit()
        print("Users have been added to the database.")

def populate_countries():
    # Example data for new countries
    with app.app_context():
        countries_data = [
            {"name": "United States", "code": "US"},
            {"name": "United Kingdom", "code": "UK"},
            {"name": "France", "code": "FR"},
            # Add more countries as needed
        ]

        # Create and add each country to the session
    
        for data in countries_data:
            new_country = Country(**data)
            db.session.add(new_country)

        # Commit all changes to the database
        db.session.commit()

        return countries_data  # Optionally return the list of countries data

def populate_cities():
    with app.app_context():
        cities_data = [
            {"name": "New York", "country_code": "US"},
            {"name": "Toronto", "country_code": "CA"},
            {"name": "Berlin", "country_code": "DE"},
            # Add more cities as needed
        ]
        
        for city_data in cities_data:
            country = Country.get(city_data["country_code"])
            if country:
                city = City.query.filter_by(name=city_data["name"]).first()
                if not city:
                    new_city = City(name=city_data["name"], country_code=country.code)
                    db.session.add(new_city)
        
        print("Cities have been added to the database.")
        db.session.commit()
