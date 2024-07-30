from typing import Type, TypeVar, Generic, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from qna_api.core.database import get_db

T = TypeVar('T')

class BaseRepository(Generic[T]):
    _instance = None

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db
        
    def get(self, id: int) -> T:
        return self.db.query(self.model).get(id)

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, obj: T) -> T:
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            self.db.rollback()
            self.refresh_db()
            raise ValueError(self._parse_integrity_error(e))

    def update(self, obj: T) -> T:
        try:
            self.db.merge(obj)
            self.db.commit()
            return obj
        except IntegrityError as e:
            self.db.rollback()
            self.refresh_db()
            raise ValueError(self._parse_integrity_error(e))

    def delete(self, id: int) -> None:
        obj = self.get(id)
        self.db.delete(obj)
        self.db.commit()

    def refresh_db(self):
        self.db = next(get_db())

    def _parse_integrity_error(self, error: IntegrityError) -> str:
        orig_msg = str(error.orig)
        err_msg = orig_msg.split(':')[-1].replace('\n', '').strip()

        parts = err_msg.split('.')
        if len(parts) >= 2:
            table, column = parts[-2], parts[-1]
            return f"Duplicate entry for {column} in {table}. Please choose a different value."
        else:
            return "An error occurred while processing your request."
