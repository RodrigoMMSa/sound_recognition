from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sqla
import logging as log


base = declarative_base()


class Song(base):
    __tablename__ = "songs"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    name = sqla.Column(sqla.String(length=255), nullable=False)
    fingerprinted = sqla.Column(sqla.Boolean, default=False)
    file_sha1 = sqla.Column(sqla.Binary(length=20), nullable=False)


class Fingerprint(base):
    __tablename__ = "fingerprints"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    hash = sqla.Column(sqla.Binary(length=10), nullable=False)
    song_id = sqla.Column(
        sqla.Integer, sqla.ForeignKey(Song.id, ondelete="CASCADE"), nullable=False
    )
    offset = sqla.Column(sqla.Integer, nullable=False)

    unique = sqla.UniqueConstraint('hash', 'song_id', 'offset')


class Database(object):
    def __init__(self, url):
        super(Database, self).__init__()
        self.url = url
        log.info("Linking to 'songs' Database")
        self.engine = sqla.create_engine(url)
        self.session = sessionmaker(bind=self.engine)()
        base.metadata.create_all(self.engine)

        # clean by deleting not fully fingerprinted songs (it could have been abruptly killed on previous run)
        self.session.query(Song).filter(Song.fingerprinted.is_(False)).delete()
        self.session.commit()
