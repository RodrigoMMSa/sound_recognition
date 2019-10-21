from .database import Database
import logging as log


log.basicConfig(level=log.INFO)
log.info('Started')


class Project:
    confidence = 'confidence'
    match_time = 'match_time'
    offset = 'offset'
    db = Database('sqlite:///songs.db')
    fingerprint_limit = None

    def get_fingerprinted_songs(self):
        # Find previously indexed sounds
        pass
