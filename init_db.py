from database import Base, engine

# This will create the database file and tables if they don't exist
Base.metadata.create_all(bind=engine)

print("✅ Database and tables created successfully.")
