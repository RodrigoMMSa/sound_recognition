import logging as log
from Project import Main
from signal import signal, SIGINT


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    log.info('Finished')
    exit(0)


if __name__ == '__main__':
    log.info('Started press CTRL-C to exit')
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    # Running Project on INFO
    police = Main()
    # Fingerprint all the mp3's in the directory we give it
    police.fingerprint_directory("Audio_files", [".mp3"])

    while True:
        police.recognize()
