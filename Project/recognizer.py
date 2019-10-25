from Project.fingerprint import *
import numpy as np
import pyaudio
import logging as log
import audioop


class MicrophoneRecognizer:
    default_chunksize = 8192
    default_format = pyaudio.paInt16
    default_channels = 2
    default_samplerate = 44100
    default_treshold = 50

    def __init__(self, main):
        self.audio = pyaudio.PyAudio()
        self.data = []
        self.channels = MicrophoneRecognizer.default_channels
        self.chunksize = MicrophoneRecognizer.default_chunksize
        self.samplerate = MicrophoneRecognizer.default_samplerate
        self.recorded = False
        self.main = main
        self.Fs = DEFAULT_FS
        self.stream_loud = None
        self.stream = None
        self.rms_val = 0

    def listen(self):
        print('Listening beginning')
        self.stream_loud = self.audio.open(
            format=self.default_format,
            channels=self.channels,
            rate=self.samplerate,
            input=True,
            frames_per_buffer=self.chunksize,
        )
        security = True
        while security:
            inout = self.stream_loud.read(self.chunksize, exception_on_overflow=False)
            self.rms_val = audioop.rms(inout, 2)  # width=2 for format=paInt16
            if self.rms_val > self.default_treshold:
                log.info('sound: %d' % self.rms_val)
                self.stream_loud.stop_stream()
                self.stream_loud.close()
                security = False
                self.recognize()

    def _recognize(self, *data):
        matches = []
        for d in data:
            matches.extend(self.main.find_matches(d, Fs=self.Fs))
        return self.main.align_matches(matches)

    def start_recording(self):
        print('Starting recording')
        self.stream = self.audio.open(
            format=self.default_format,
            channels=self.channels,
            rate=self.samplerate,
            input=True,
            frames_per_buffer=self.chunksize,
        )
        self.recorded = False
        self.data = [[] for i in range(self.channels)]

    def process_recording(self):
        data = self.stream.read(self.chunksize, exception_on_overflow=False)
        nums = np.fromstring(data, np.int16)
        for c in range(self.channels):
            self.data[c].extend(nums[c::self.channels])

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.recorded = True

    def recognize_recording(self):
        if not self.recorded:
            raise log.info("Recording was not complete/begun")
        return self._recognize(*self.data)

    def get_recorded_time(self):
        return len(self.data[0]) / self.samplerate

    def recognize(self, seconds=1.5):
        self.start_recording()
        for i in range(0, int(self.samplerate / self.chunksize * seconds)):
            self.process_recording()
        self.stop_recording()
        return self.recognize_recording()
