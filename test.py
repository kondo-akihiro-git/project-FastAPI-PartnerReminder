from typing import Optional

from sqlalchemy import Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Meetings(Base):
    __tablename__ = 'meetings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='meetings_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(Text)
    events: Mapped[Optional[str]] = mapped_column(Text)
    partner_looks: Mapped[Optional[str]] = mapped_column(Text)
    talked_topics: Mapped[Optional[str]] = mapped_column(Text)
    good_points: Mapped[Optional[str]] = mapped_column(Text)
    next_preparation: Mapped[Optional[str]] = mapped_column(Text)
    self_look_image: Mapped[Optional[str]] = mapped_column(Text)


class TestTable(Base):
    __tablename__ = 'test_table'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='test_table_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_title: Mapped[str] = mapped_column(Text)
    test_note: Mapped[Optional[str]] = mapped_column(Text)
