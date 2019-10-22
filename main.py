import logging as log
from Project import Main


if __name__ == '__main__':
    log.info('Started')
    # Running Project on INFO
    police = Main()
    # Fingerprint all the mp3's in the directory we give it
    police.fingerprint_directory("Audio_files", [".mp3"])
    
    secs = 15
    sound = police.recognize(seconds=secs)
    if sound is None:
        print(
            "Nothing recognized -- did you play the sound out loud so your mic could hear it? :)"
        )
    else:
        print("From mic with %d seconds we recognized: %s\n" % (secs, sound))
    log.info('Finished')
