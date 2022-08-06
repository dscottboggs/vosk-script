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
 - Download [this script](https://raw.githubusercontent.com/dscottboggs/vosk-script/master/vosk-script.py)
   
   It can go anywhere, just run it like `python /full/path/to/vosk-script.py`.
   However, you can also place it in a folder on your `$PATH`, such as
   `~/.local/bin`, and make it executable, then you will be able to run just
   `vosk-script.py` from anywhere. Like so:
~~~
$ curl https://raw.githubusercontent.com/dscottboggs/vosk-script/master/vosk-script.py > ~/.local/bin/vosk-script.py
$ chmod 755 ~/.local/bin/vosk-script.py
~~~
 - Download and unzip a model from
   [this page](https://alphacephei.com/vosk/models). For example:
~~~
$ mkdir ~/.local/share/vosk-models
$ cd ~/.local/share/vosk-models
$ wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
$ unzip vosk-model-en-us-0.22.zip
$ ln -s vosk-model-en-us-0.22 english
~~~
 - Run the script. Run `./vosk-script.py --help` for more information.
