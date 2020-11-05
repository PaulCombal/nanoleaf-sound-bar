Nanoleaf sound bar
===

# Setup

I set up a virtualenv to run this script, but you can do without.

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