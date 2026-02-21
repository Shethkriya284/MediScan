from app import app, db
from app import Dependent

with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("Tables created successfully.")
    
    # Verify if table exists by trying a query
    try:
        count = Dependent.query.count()
        print(f"Dependent table exists. Count: {count}")
    except Exception as e:
        print(f"Error accessing Dependent table: {e}")
