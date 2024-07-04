""" Another way to run the app"""

# hbnb.py
from src import create_app, db
from src.database import db_session, init_db
from populate import populate_users, populate_countries, populate_cities
app = create_app()

def get_db_tables():
    with app.app_context():
        metadata = db.MetaData()
        metadata.reflect(bind=db.engine)
        return metadata.tables.keys()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    init_db()
    with app.app_context():
        db.create_all()
        print("Database tables created.")

    print(get_db_tables())
    # Optionally, you can populate users after fetching them
    # populate_users()
    # populate_countries()
    # populate_cities()

    # Run the Flask application
    app.run()


