# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # 1. Create the SQLite Database File
# SQLALCHEMY_DATABASE_URL = "sqlite:///./ulinzi.db"

# # 2. Create the Engine
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# # 3. Create a Session Factory (To talk to the DB)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 4. The Base Class for our Tables
# Base = declarative_base()

# # Dependency to get the DB session in API routes
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()