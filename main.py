import logging as log
from Project import Main

if __name__ == '__main__':
    log.info('Started')
    # Running Project on INFO
    police = Main()
    # Fingerprint all the mp3's in the directory we give it
    police.fingerprint_directory("Audio_files", [".mp3"])
    log.info('Finished')
