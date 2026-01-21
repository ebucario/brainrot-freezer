"""handles gpio buttons / triggers"""

import gpiozero

from . import sound

def _handle_button():
	sound.play_sound()

button = gpiozero.Button(2, bounce_time=0.1)
button.when_released = _handle_button