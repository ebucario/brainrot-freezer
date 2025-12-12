# brainrot freezer

this repo holds a python script that randomly plays sounds when triggered by a GPIO pin (such as on a raspberry pi). it uses `gpiozero` to poll the GPIO and `pygame` to play the sounds (since `playsound` doesn't work on raspberry pi's).

## install

1. clone this repository to a folder.
1. \[Optional\] setup a virtual environment.
   - `python -m venv .venv`
   - `. ./.venv/bin/activate` (or `./.venv/bin/activate.bat` on Windows)
1. `pip install -r requirements.txt`
1. create a `sounds` folder and put sounds (OGG or WAV, per [pygame docs](https://www.pygame.org/docs/ref/mixer.html?highlight=sound#pygame.mixer.Sound)) in it, or else edit `app.py` to point to a different sounds folder.
1. `python app.py`