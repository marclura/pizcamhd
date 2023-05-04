# PIZCAMHD
# https://github.com/marclura/pizcamhd

#!/bin/python

import picamera
import RPi.GPIO as GPIO
import time
import os
import psutil
from flask import Flask, render_template

GPIO.setmode(GPIO.BCM)


try:
	camera = picamera.PiCamera()
	camera.framerate = 30
	camera.vflip = True
	camera.hflip = True
	camera.start_preview()

except:
	print('ERROR: Camera NOT started!')

else:
	print('OK: Camera started!')

app = Flask(__name__)


@app.route('/')
def index():
	templateData = {
		'title': 'pizcamhd1',
	}
	return render_template('pizcamhd.html', **templateData)

@app.route('/<actionid>')
def handleRequest(actionid):
	print('Action id: {}'.format(actionid))
	if(actionid == 'vflip'):
		if (camera.vflip):
			camera.vflip = False
		else:
			camera.vflip = True
	elif (actionid == 'hflip'):
		if (camera.hflip):
			camera.hflip = False
		else:
			camera.hflip = True
	elif (actionid == 'start_preview'):
		if (camera.previewing):
			camera.stop_preview()
		else:
			camera.start_preview()

	if(actionid == 'video_denoise'):
		if(camera.video_denoise):
			camera.video_denoise = False
		else:
			camera.video_denoise = True

	if(actionid == 'video_stabilization'):
		if(camera.video_stabilization):
			camera.video_stabilization = False
		else:
			camera.video_stabilization = True

	# AWB
	search = 'awb_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.awb_mode = val

	# ISO
	search = 'iso_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.iso = val

	# Exposure mode
	search = 'exp_mode_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.exposure_mode = val

	# DRC strength
	search = 'drc_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.drc_strength = val

	# Meter mode
	search = 'meter_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.meter_mode = val


	return 'OK 200'


if __name__ == '__main__':

	app.run(debug=True, port=80, host='0.0.0.0')






