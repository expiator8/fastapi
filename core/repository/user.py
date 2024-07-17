from sqlalchemy.orm import Session
from api.v1.models import user as user_models
from ..entity import user as user_entity


class UserRepository:
    def get_user_by_email(
        db: Session,
        email: str,
    ) -> user_entity.User | None:
        return (
            db.query(user_entity.User).filter(user_entity.User.email == email).first()
        )

    def create_user(
        db: Session,
        user: user_models.UserCreate,
    ) -> user_entity.User:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = user_entity.User(
            username=user.username,
            email=user.email,
            hashed_password=fake_hashed_password,
        )
        db.add(db_user)
        db.commit()
        return db_user
