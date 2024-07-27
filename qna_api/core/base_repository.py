from typing import Type, TypeVar, Generic, List
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get(self, id: int) -> T:
        return self.db_session.query(self.model).get(id)

    def get_all(self) -> List[T]:
        return self.db_session.query(self.model).all()

    def create(self, obj: T) -> T:
        self.db_session.add(obj)
        self.db_session.commit()
        self.db_session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.db_session.merge(obj)
        self.db_session.commit()
        return obj

    def delete(self, id: int) -> None:
        obj = self.get(id)
        self.db_session.delete(obj)
        self.db_session.commit()