import socket, select, time
from pygame import mixer
import  RPi.GPIO as GPIO
import os

####################################################
#### Raspberry pi - Pin configurations    ##########
####################################################
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT) 							# Drone-LED
GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_UP) 	# Drone-Push-button

GPIO.setup(22, GPIO.OUT) 							# Ambulance-LED
GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP) 	# Ambulance-Push-button

## Server (IP, port)
host = '127.0.0.1'
port = 5005

#To play sounds
mixer.init()

def instruct_drone():
	while True:
		input1 = GPIO.input(4)
		if input1 == 0:
			GPIO.output(17,True)
			print("Sending an Drone to crash site")
			mixer.music.load("drone.mp3")
			mixer.music.play()
			drone_surverlliance()
			break
		else:
			GPIO.output(17,False)
		time.sleep(0.2)
	
	time.sleep(6)
	GPIO.output(17,False)

def drone_surverlliance():
	os.popen("raspivid -o video.h264 -t 10000")
	
	
def instruct_ambulance():
	while True:
		input2 = GPIO.input(27)
		if input2 == 0:
			GPIO.output(22,True)
			print("Sending an Ambulance to crash site")
			mixer.music.load("ambulance.wav")
			mixer.music.play()
			break
		else:
			GPIO.output(22,False)
			
		time.sleep(0.2)

	time.sleep(6)
	GPIO.output(22,False)

def execute_help():
	print("Waiting instruction to send a Drone")
	instruct_drone()
	print("Waiting instruction to send an ambulance")
	instruct_ambulance()
	
def report_crash_to_nearby_cars(connected_cars):
	for c in connected_cars:
		c.send("A crash in nearby vicinity .. Proceed with caution")

# Starting the service
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
my_sockets = [s]
connected_cars = []


if len(my_sockets)==1:
	print "Waiting for Cars to report"

try:
	while 1:
		infds, outfds, errfds = select.select(my_sockets, [], [], 1)
		#print("infds, outfds, errfds", len(infds), len(outfds), len(errfds))
		
		if len(infds) != 0:
			#print 'enter infds'    
			for fds in infds:
				if fds == s:
					clientsock, clientaddr = fds.accept()
					my_sockets.append(clientsock)
					connected_cars.append(clientsock)
					print 'connect from:', clientaddr
				else:
					try:
						print("Data from client")
						data = fds.recv(1024)

						if not data:
							print time.asctime(), " ", "Connection closed by the car"
							my_sockets.remove(fds)
							fds.close()
						else:
							#if data == "Car crash":
							print time.asctime(), " ", "Message from road:", data
							fds.send("OK. Sending help to you")
							report_crash_to_nearby_cars(connected_cars)
							print time.asctime(), " ", "Responded to crash incidence"
							execute_help()
					except:
						#print time.asctime(), " ", "Connection closed by the car"
						my_sockets.remove(fds)
						fds.close()
					
					
			if len(outfds) != 0:
				pass
				#print 'enter outfds'   
				#for fds in outfds:
				#        fds.send("python select server from Debian.\n")
		
			if len(errfds) != 0:
				print("Exception in socket detected")
except:
	print("Exception detected .. Closing the controller")
	GPIO.cleanup()
	s.close()

#if __name__=="__main__":
#	run_controller()

