from cgi import parse_multipart, print_arguments
from code import interact
from os import cpu_count
from time import CLOCK_REALTIME
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artsits.id"))
    album_id = Column(Integer, ForeignKey("artists.id"))
    track_numer = Column(Integer)
    track_denom = Column(Integer)
    disc_numer = Column(Integer)
    disc_denom = Column(Integer)
    year = Column(Integer)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    songs = relationship("Song", backref="artist")
    albums = relationship("Album", backref="album_artist")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    album_artist_id = Column(Integer, ForeignKey("artists.id"))
    name = Column(String)

    songs = relationship("Song", backref="album")
