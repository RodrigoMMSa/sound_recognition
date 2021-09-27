from .database import Database
import logging as log
import binascii
import multiprocessing
import sys
import Project.decoder
import os
import traceback
from Project.fingerprint import *
from Project.recognizer import MicrophoneRecognizer

log.basicConfig(level=log.INFO)


class Main:
    confidence = 'confidence'
    match_time = 'match_time'
    offset = 'offset'
    db = Database('sqlite:///sounds.db')
    fingerprint_limit = None
    sounds = None
    soundhashes_set = {}
    sound = ""

    def __init__(self):
        self.get_fingerprinted_sounds()

    def get_fingerprinted_sounds(self):
        # get sounds previously indexed
        self.sounds = self.db.get_sounds()
        self.soundhashes_set = set()  # to know which ones we've computed before
        for sound in self.sounds:
            sound_hash = binascii.hexlify(sound.file_sha1).upper().decode('utf-8')
            self.soundhashes_set.add(sound_hash)

    def fingerprint_directory(self, path, extensions, nprocesses=None):
        # Try to use the maximum amount of processes if not given.
        try:
            nprocesses = nprocesses or multiprocessing.cpu_count()
        except NotImplementedError:
            nprocesses = 1
        else:
            nprocesses = 1 if nprocesses <= 0 else nprocesses

        pool = multiprocessing.Pool(nprocesses)

        filenames_to_fingerprint = []
        for filename, _ in decoder.find_files(path, extensions):
            log.info('looking for {} file in the {} path'.format(filename, path))

            # don't "re-fingerprint" already fingerprinted files
            if decoder.unique_hash(filename) in self.soundhashes_set:
                log.info(
                    "%s already fingerprinted, continuing..." % filename
                )
                continue

            filenames_to_fingerprint.append(filename)

        # Prepare _fingerprint_worker input
        worker_input = list(
            zip(
                filenames_to_fingerprint,
                [self.fingerprint_limit] * len(filenames_to_fingerprint)
            )
        )

        # Send off our tasks
        iterator = pool.imap_unordered(_fingerprint_worker, worker_input)

        # Loop till we have all of them
        while True:
            try:
                sound_name, hashes, file_hash = next(iterator)
            except multiprocessing.TimeoutError:
                continue
            except StopIteration:
                break
            except FileExistsError:
                log.error("Failed fingerprinting")
                # Print traceback because we can't re-raise it here
                traceback.print_exc(file=sys.stdout)
            else:
                sid = self.db.insert_sound(sound_name, file_hash)

                self.db.insert_hashes(sid, hashes)
                self.db.set_sound_fingerprinted(sid)
                self.get_fingerprinted_sounds()

        pool.close()
        pool.join()

    def recognize(self, *options, **kwoptions):
        r = MicrophoneRecognizer(self)
        return r.listen()

    def find_matches(self, samples, Fs=DEFAULT_FS):
        hashes = fingerprint(samples, fs=Fs)
        return self.db.return_matches(hashes)

    def align_matches(self, matches):
        """
            Finds hash matches that align in time with other matches and finds
            consensus about which hashes are "true" signal from the audio.

            Returns a dictionary with match information.
        """
        # align by diffs
        diff_counter = {}
        largest = 0
        largest_count = 0
        sound_id = -1
        for tup in matches:
            sid, diff = tup
            if diff not in diff_counter:
                diff_counter[diff] = {}
            if sid not in diff_counter[diff]:
                diff_counter[diff][sid] = 0
            diff_counter[diff][sid] += 1

            if diff_counter[diff][sid] > largest_count:
                largest = diff
                largest_count = diff_counter[diff][sid]
                sound_id = sid

        # extract identification
        if (self.db.get_sound_by_id(sound_id)) and (largest_count > 10):
            self.sound = self.db.get_sound_by_id(sound_id)
            soundname = self.sound.name
            # return match info
            nseconds = round(float(largest) / DEFAULT_FS * DEFAULT_WINDOW_SIZE * DEFAULT_OVERLAP_RATIO, 5)
            sha1 = binascii.hexlify(self.sound.file_sha1).decode('utf-8')
            self.sound = "We heard a {}!!\n with a confidence of {}, file_sha1 {} in {}".format(soundname,
                                                                                                largest_count,
                                                                                                sha1,
                                                                                                nseconds)
            # sound = {
            #     'sound_id': sound_id,
            #     'sound_name': soundname,
            #     Main.confidence: largest_count,
            #     Main.offset: int(largest),
            #     'offset_seconds': nseconds,
            #     'file_sha1': binascii.hexlify(self.sound.file_sha1).decode('utf-8'),
            # }
        elif self.sound == "Cuidado, som muito alto":
            pass
        else:
            self.sound = "Som normal"
        print(self.sound)
        return self.sound
    

def _fingerprint_worker(filename, limit=None, sound_name=None):
    # Pool.imap sends arguments as tuples so we have to unpack them ourselves.
    try:
        filename, limit = filename
    except ValueError:
        pass

    soundname, extension = os.path.splitext(os.path.basename(filename))
    sound_name = sound_name or soundname
    channels, fs, file_hash = decoder.read(filename, limit)
    result = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        log.info(
            (
                "Fingerprinting channel %d/%d for %s" %
                (channeln + 1, channel_amount, filename)
            )
        )
        hashes = fingerprint(channel, fs=fs)
        log.info(
            (
                "Finished channel %d/%d for %s" %
                (channeln + 1, channel_amount, filename)
            )
        )
        result |= set(hashes)

    return sound_name, result, file_hash
