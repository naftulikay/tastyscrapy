#!/usr/bin/env python3

from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Table, Text
)
from sqlalchemy.ext.declarative import declarative_base as Base
from sqlalchemy.orm import relationship


bookmark_tag_table = Table('bookmark_tag', Base.metadata,
    Column(Integer, primary_key=True),
    Column('bookmark_id', Integer, ForeignKey('bookmark.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')),
)


class Bookmark(Base):
    __tablename__ = "bookmark"

    id = Column(Integer, primary_key=True)
    url = Column(String, index=True, unique=True)
    title = Column(String)
    comment = Column(Text)
    private = Column(Boolean)
    # many to many via bookmark_tag_table
    tags = relationship("Tag", secondary=bookmark_tag_table,
        back_populates="bookmarks")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    # many to many via bookmark_tag_table
    bookmarks = relationship("Bookmark", secondary=bookmark_tag_table,
        back_populates="tags")
