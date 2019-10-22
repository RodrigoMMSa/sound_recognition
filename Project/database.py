from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sqla
import logging as log
import binascii


base = declarative_base()


class Sound(base):
    __tablename__ = "sound"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    name = sqla.Column(sqla.String(length=255), nullable=False)
    fingerprinted = sqla.Column(sqla.Boolean, default=False)
    file_sha1 = sqla.Column(sqla.Binary(length=20), nullable=False)


class Fingerprint(base):
    __tablename__ = "fingerprints"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    hash = sqla.Column(sqla.Binary(length=10), nullable=False)
    sound_id = sqla.Column(
        sqla.Integer, sqla.ForeignKey(Sound.id, ondelete="CASCADE"), nullable=False
    )
    offset = sqla.Column(sqla.Integer, nullable=False)

    unique = sqla.UniqueConstraint('hash', 'sound_id', 'offset')


class Database(object):
    def __init__(self, url):
        super(Database, self).__init__()
        self.url = url
        self.engine = sqla.create_engine(url)
        self.session = sessionmaker(bind=self.engine)()
        base.metadata.create_all(self.engine)

        # clean by deleting not fully fingerprinted sounds (it could have been abruptly killed on previous run)
        self.session.query(Sound).filter(Sound.fingerprinted.is_(False)).delete()
        self.session.commit()

    def get_sounds(self):
        """Returns all fully fingerprinted sounds in the database."""
        return self.session.query(Sound).filter(Sound.fingerprinted)
    
    def insert_sound(self, sound_name, file_hash):
        """
        Inserts a sound name into the database, returns the new
        identifier of the sound.

        :param sound_name: name of the sound
        :param file_hash: sha1 hex digest of the filename
        """
        sound = Sound(name=sound_name, file_sha1=binascii.unhexlify(file_hash))
        self.session.add(sound)
        self.session.commit()
        return sound.id

    def insert_hashes(self, sid, hashes):
        """
        Insert a multitude of fingerprints.

        :param sid: sound identifier the fingerprints belong to
        :param hashes: A sequence of tuples in the format (hash, offset)
            hash: Part of a sha1 hash, in hexadecimal format
            offset: Offset this hash was created from/at.
        """
        fingerprints = []
        for sha, offset in set(hashes):
            fingerprints.append(
                Fingerprint(
                    hash=binascii.unhexlify(sha),
                    sound_id=sid,
                    offset=int(offset)
                )
            )

        self.session.bulk_save_objects(fingerprints)
        
    def set_sound_fingerprinted(self, sid):
        """
        Marks a sound as having all fingerprints in the database.

        :param sid: sound identifier
        """
        sound = self.session.query(Sound).filter(Sound.id == sid).one()
        sound.fingerprinted = True
        self.session.commit()
