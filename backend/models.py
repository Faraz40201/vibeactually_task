from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    wing = Column(String, nullable=True)
    team = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="member")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False)   # <-- instead of many columns
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    member_id = Column(Integer, ForeignKey("members.id"))
    member = relationship("Member", back_populates="tasks")
