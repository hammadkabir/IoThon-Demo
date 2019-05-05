 #!/usr/bin/env python
import socket, time
from pygame import mixer
import  RPi.GPIO as GPIO

##################################################
#### Micro-controller pins for crash accident ####
##################################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP) # Accident-push-button
GPIO.setup(24, GPIO.OUT) 	# Accident-LED

##################################################
######## Connection to control center ############
##################################################

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Car crash @ GPS coordinates (27.343, 43.232)"

# To play sounds
mixer.init()


def evaluate_help_button():
	while True:
		input2 = GPIO.input(23)
		if input2 == 0:
			GPIO.output(24,True)
			print("Reporting crash incident")
			report_crash_incident()
			
			mixer.music.load("car_crash.mp3")
			mixer.music.play()
			break
		else:
			GPIO.output(24,False)
			
		time.sleep(0.2)

	time.sleep(6)
	GPIO.output(24,False)

def connect_controllCenter():
	""" Connects to control center """
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	return s

def report_crash_incident():
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	print time.asctime(), " ", "Control center has responded to query"
	if data == "OK. Sending help to you":
		print time.asctime(), " ", "Crash acknowledged"

def close_connection(s):
	s.close()
	
if __name__=="__main__":
	try:
		s = connect_controllCenter()
		print time.asctime(), " ", "Press button to report crash"
		#report_crash_incident()
		evaluate_help_button()
		close_connection(s)
	except:
		print "Exception.. Closing program"
		

