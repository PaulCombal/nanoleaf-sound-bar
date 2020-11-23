Nanoleaf sound bar
===

# Installation

If you're not familiar with command line or Python here's a step-by-step guide on how to run this on a Raspberry Pi.
If you know what you're doing, you probably won't need to read this.
After running `$ git clone (repo)`, use `cd` to move into the cloned repository folder.
* Run `$ python -m venv .`.
* Run `source bin/activate`
* Run `pip install requests sounddevice numpy python-dotenv nanoleafapi`

If you get an error message mentionning 'PortAudio library not found', you will need to run `$ sudo apt install libportaudio2` in another terminal.
Similarly, if you get an error mentionning 'libfs77blas.so.x', please run `$ sudo apt install libatlas-base-dev` in a separate terminal.

# Configuration

`$ cp .env.template .env`

In `.env`, fill in the missing properties:
* API_KEY: the token you get from your nanoleaf after pairing with it and maintaining the power button for 6-7 seconds
* NANOLEAF_IP: The IP and port of your Nanoleaf. Eg: `10.42.0.224:16021`
* NANOLEAF_IP_PORTLESS: Same as above, but omitting the port number. Eg: `10.42.0.224`

Adjust sensibility based on your microphone. Edit the colors used as you wish.

Connect the canvas in the order of the sound bar path. Personnally, I always start with the main station.

# Logging

Set ENABLE_LOGS to 1 for logging. MAX_LOGS_LENGTH is the max amount of lines your logfile will have

The log is in this format: `<epoch timestamp>,<mic volume>\n`