import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from qna_api.core.database import get_db
from qna_api.core.base_repository import BaseRepository
from typing import Type, TypeVar

T = TypeVar('T')

class MockModel:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def base_repository(db_session):
    return BaseRepository(MockModel, db_session)

def test_get(base_repository, db_session):
    mock_obj = MockModel(id=1, name="Test")
    db_session.query().get.return_value = mock_obj

    result = base_repository.get(1)
    assert result == mock_obj
    db_session.query().get.assert_called_once_with(1)

def test_get_all(base_repository, db_session):
    mock_objs = [MockModel(id=1, name="Test1"), MockModel(id=2, name="Test2")]
    db_session.query().all.return_value = mock_objs

    result = base_repository.get_all()
    assert result == mock_objs
    db_session.query().all.assert_called_once()

def test_create(base_repository, db_session):
    mock_obj = MockModel(id=1, name="Test")
    db_session.add.side_effect = lambda x: setattr(x, 'id', 1)
    db_session.commit.return_value = None
    db_session.refresh.return_value = None

    result = base_repository.create(mock_obj)
    assert result.id == 1
    db_session.add.assert_called_once_with(mock_obj)
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(mock_obj)

def test_create_integrity_error(base_repository, db_session):
    mock_obj = MockModel(name="Test")
    db_session.add.side_effect = IntegrityError("mock", "params", "orig")
    db_session.rollback.return_value = None

    with patch.object(base_repository, 'refresh_db') as refresh_db_mock:
        with pytest.raises(ValueError):
            base_repository.create(mock_obj)
        db_session.rollback.assert_called_once()
        refresh_db_mock.assert_called_once()

def test_update(base_repository, db_session):
    mock_obj = MockModel(id=1, name="Updated Test")
    db_session.merge.return_value = mock_obj
    db_session.commit.return_value = None

    result = base_repository.update(mock_obj)
    assert result == mock_obj
    db_session.merge.assert_called_once_with(mock_obj)
    db_session.commit.assert_called_once()

def test_update_integrity_error(base_repository, db_session):
    mock_obj = MockModel(id=1, name="Updated Test")
    db_session.merge.side_effect = IntegrityError("mock", "params", "orig")
    db_session.rollback.return_value = None

    with patch.object(base_repository, 'refresh_db') as refresh_db_mock:
        with pytest.raises(ValueError):
            base_repository.update(mock_obj)
        db_session.rollback.assert_called_once()
        refresh_db_mock.assert_called_once()

def test_delete(base_repository, db_session):
    mock_obj = MockModel(id=1, name="Test")
    db_session.query().get.return_value = mock_obj
    db_session.delete.return_value = None
    db_session.commit.return_value = None

    base_repository.delete(1)
    db_session.delete.assert_called_once_with(mock_obj)
    db_session.commit.assert_called_once()

def test_refresh_db(base_repository):
    with patch('qna_api.core.base_repository.get_db', return_value=iter([MagicMock()])):
        base_repository.refresh_db()
        assert base_repository.db is not None

def test_parse_integrity_error(base_repository):
    error_message = "UNIQUE constraint failed: table.column"
    integrity_error = IntegrityError(statement="mock_statement", params="mock_params", orig=Exception(error_message))
    
    parsed_message = base_repository._parse_integrity_error(integrity_error)
    assert parsed_message == "Duplicate entry for column in table. Please choose a different value."

