#!/usr/bin/env python3
# requires python 3.9+
from vosk import Model, KaldiRecognizer as Recongizer, SetLogLevel
from os import path, environ, listdir
from sys import stderr, stdout, argv
from subprocess import Popen, PIPE
from pathlib import Path
from json import loads
from progress.spinner import PixelSpinner as Spinner

MODELS_DIR = Path.home() / ".local" / "share" / "vosk-models"
default_model = MODELS_DIR / "english"

spinner = Spinner(file=stderr)
p = spinner.next

def available_models():
    return listdir(MODELS_DIR)


def run(model_location,
        source_file,
        destination,
        sample_rate=16_000):

    model = Model(str(model_location))
    recognizer = Recongizer(model, sample_rate)
    process = Popen(
        popen_args(source_file, sample_rate),
        stdout=PIPE
    )
    p()
    while data := process.stdout.read(0x1000):
        p()
        if recognizer.AcceptWaveform(data):
            destination.write(
                loads(
                    recognizer.Result()
                )['text'] + '\n'
            )
        p()
    destination.write(f'{loads(recognizer.FinalResult())["text"]}\n')
    spinner.finish()

def popen_args(source_file, sample_rate):
    return [
        'ffmpeg', '-loglevel', 'quiet',
        '-i', source_file,
        '-ar', str(sample_rate),
        '-ac', '1',
        '-f', 's16le',
        '-' # output to stdout
    ]

def run_from_args(argv):
    if len(argv) == 1:
        print('please specify a source file. STDIN is not yet supported')
        exit(1)
    if len(argv) == 2:
        if argv == '--list-models':
            print('', *available_models(), sep='\n - ')
            exit()
        run(default_model, argv[1], stdout)
        exit()

    model_location, source_file, destination = None, None, None
    argv.pop(0) # command name
    while argv:
        arg = argv.pop(0)
        if arg in {'-m', '--model'}:
            model_location = MODELS_DIR / argv.pop(0)
        elif arg in {'-i', "--in"}:
            source_file = argv.pop(0)
        elif arg in {'-o', '--out', '--destination'}:
            destination = argv.pop(0)
        else:
            print(f'unrecognized option "{arg}"')
            exit(2)
    if destination is None:
        run(model_location or default_model, source_file, stdout)
    else:
        with open(destination, 'w') as destination_file:
            run(model_location or default_model, source_file, destination_file)

if __name__ == '__main__':
    stderr.write(f'{argv=}\n')
    run_from_args(argv)
