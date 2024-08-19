# PIZCAMHD
# https://github.com/marclura/pizcamhd

#!/bin/python

import picamera
import RPi.GPIO as GPIO
import time
import os
import socket
import netifaces
from datetime import datetime
from flask import Flask, render_template


camera_name = 'pizcamhd1'
rotation = 0
old_btn_rotate = 0


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # set up GPIO numbering

GPIO.setup(17, GPIO.IN) # rotate
GPIO.setup(27, GPIO.IN) # power off
GPIO.setup(22, GPIO.OUT) # led

'''
addrs = netifaces.ifaddresses('wlan0')
ip_address = addrs[netifaces.AF_INET][0]['addr']
'''

camera = picamera.PiCamera()

def rotate():
	if rotation == 0:
			camera.hflip = False
			camera.vflip = False
	elif rotation == 1:
			camera.vflip = True
	elif rotation == 2:
			camera.hflip = True
	elif rotation == 3:
			camera.vflip = False



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
			GPIO.output(22, 0)
		else:
			camera.start_preview()
			GPIO.output(22, 1)

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
		camera.iso = int(val)

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

	# Image effect
	search = 'image_effect_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.image_effect = val

	# brightness
	search = 'brightness_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.brightness = int(val)

	# saturation
	search = 'saturation_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.saturation = int(val)

	# brightness
	search = 'brightness_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.brightness = int(val)

	# contrast
	search = 'contrast_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.contrast = int(val)

	# exposure_compensation
	search = 'exposure_compensation_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.exposure_compensation = int(val)

	# shutter_speed
	search = 'shutter_speed_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.shutter_speed = int(val)

	# sharpness
	search = 'sharpness_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.sharpness = int(val)

	# sharpness
	search = 'framerate_'
	index = actionid.find(search)

	if(index != -1):
		val = actionid[len(search): len(actionid)]
		print(val)
		camera.stop_preview()
		camera.framerate = int(val)
		camera.start_preview()


	# Capture image
	path = 'capture/'
	if(actionid == 'capture_image'):
		date = datetime.now()
		output_file = path + camera_name + '_' + date.strftime("%d-%m-%Y") + "_" + date.strftime("%H-%M-%S") + '.png'
		print(f'capture image {output_file}')
		camera.capture(output_file, 'png')


	return 'OK 200'


if __name__ == '__main__':

	#app.run(debug=False, port=80, host=ip_address)
	app.run(debug=False, port=80, host='0.0.0.0')

	try:
		camera.framerate = 30
		camera.vflip = True
		camera.hflip = True
		camera.start_preview()
		GPIO.output(22, 1)

		while True:
			# Rotation button
			if GPIO.input(17) == 1 and  old_btn_rotate == 0:
				# print( "Rotate pressed")
				old_btn_rotate = 1
				# camera.vflip = True
				if rotation <= 2:
					rotation += 1
				else:
					rotation = 0
				rotate()
			elif GPIO.input(17) == 0 and old_btn_rotate == 1:
				old_btn_rotate = 0
				# camera.vflip = False
				# print("Rotate released")

	finally:
		GPIO.cleanup()