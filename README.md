# STT script
This is a a speech-to-text script. It's very simple and doesn't do much.

## Requirements
### Minimum
 - around 500MiB RAM
 - 40-50MiB disk space for the "small" model (assuming your locale has one), not including your source media.
### Recommended
 - 8GiB RAM (the full english model hits OOM on my 4GiB laptop)
 - 2GiB disk space. Some locales are smaller but they are all around 1-2GiB for the full-size model.

## Installation
 - Install ffmpeg
 - Install python.
 - Install vosk:
~~~
$ pip install vosk
~~~
 - Download this script
 - Download and unzip a model from
   [this page](https://alphacephei.com/vosk/models). For example:
~~~
$ mkdir ~/.local/share/vosk-models
$ cd ~/.local/share/vosk-models
$ wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
$ unzip vosk-model-en-us-0.22.zip
$ ln -s vosk-model-en-us-0.22.zip english
~~~
 - Run the script. Run `./vosk-script.py --help` for more information.
