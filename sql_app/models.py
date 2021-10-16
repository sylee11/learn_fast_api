from .database import Base
from sqlalchemy import Boolean, String, Column, Integer, ForeignKey, JSON, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from enum import IntEnum


class AnswerEnum(IntEnum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    email = Column(String(100), index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    modified_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String(2000), nullable=False)
    answer_one = Column(String(2000))
    answer_two = Column(String(2000))
    answer_third = Column(String(2000))
    answer_fourth = Column(String(2000))
    type = Column(Integer, nullable=False)
    image_path = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answer = Column(Enum(AnswerEnum), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    question = relationship('Question', lazy='joined', backref=backref('answers'))


class Examination(Base):
    __tablename__ = 'examinations'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    list_question = Column(JSON, nullable=False)
    list_answer = Column(JSON, nullable=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship('User', lazy='joined', backref=backref('examinations'))
