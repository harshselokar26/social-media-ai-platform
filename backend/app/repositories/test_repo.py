from app.db.session import SessionLocal

from app.repositories.user_repository import UserRepository

db = SessionLocal()

repo = UserRepository(db)

print(repo.exists("harsh@gmail.com"))