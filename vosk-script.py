#!/usr/bin/env python3
# requires python 3.9+
from vosk import Model, KaldiRecognizer as Recongizer, SetLogLevel
from os import path, environ, listdir
from sys import stderr, stdout, argv
from subprocess import Popen, PIPE
from pathlib import Path
from json import loads
from progress.spinner import PixelSpinner as Spinner
from textwrap import dedent

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
        '-'  # output to stdout
    ]


def usage(program_name):
    print(dedent(f'''
        {program_name} INPUT_FILE
        {program_name} [options]

    Options:
        -m MODEL, --model MODEL     The directory of the model used to process speech.
        -i INPUT, --in INPUT        The source file to transcribe
        -o DEST, --out DEST,
            --destination DEST      A file to write the transcription to.
        --list-models               Lists valid options for --model.

    Any file which can be interpreted as audio (including videos) by ffmpeg can be used as input.

    The first is the simplest usage, intended for use with shell redirection.
        {program_name} somefile.webm > somefile-transcription.txt
    A (perhaps more intuitive) equivalent usage is:
        {program_name} --in somefile.mp3 --out somefile-transcription.txt
    If a model must be specified, (for example, to transcribe an Esperanto audio file using a model located at ~/.local/share/vosk-models/vosk-model-small-eo-0.42) then you must use:
        {program_name} --model vosk-model-small-eo-0.42 --in somefile.ogg --out somefile-transcription.txt
    '''))


def run_from_args(argv):
    command_name = argv.pop(0)
    if len(argv) == 1:
        print('please specify a source file. STDIN is not yet supported')
        usage(command_name)
        exit(1)
    if "--help" in argv or "-h" in argv:
        usage(command_name)
        exit()
    if '--list-models' in argv:
        print('', *available_models(), sep='\n - ')
        exit()
    # read the single argument as an input file and output to stdout
    if len(argv) == 2:
        run(default_model, argv[1], stdout)
        exit()

    model_location, source_file, destination = None, None, None
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
            usage(command_name)
            exit(2)
    if destination is None:
        run(model_location or default_model, source_file, stdout)
    else:
        with open(destination, 'w') as destination_file:
            run(model_location or default_model, source_file, destination_file)


if __name__ == '__main__':
    stderr.write(f'{argv=}\n')
    run_from_args(argv)
