import fauxmo
import logging
import time
import sys
import requests
import RPi.GPIO as GPIO ## Import GPIO library
 
from debounce_handler import debounce_handler

mode=GPIO.getmode()
GPIO.cleanup()

servo1=7
servo2=8
relay1=9
relay2=11

sleeptime=1
musicDelay=45
servoDuty=50
servoSpeed=1  #smaller number = faster
servoFlag=1
dabloonDelay=10


GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

p = GPIO.PWM(25, 50) 
p.start(servoDuty)       


 
logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    #TRIGGERS = {"office": 52000}
    TRIGGERS = {"throw me something": 52000}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        time.sleep(musicDelay)
        if name=="Hey Alexa, throw me something":
            current = time.monotonic()
            if current - last_print >= servoSpeed:
                last_print = current
                if servoFlag==1:
                    servoDuty+=1
                    if servoDuty==100:
                        servoFlag=0
                if servoFlag==0:
                    servoDuty-=1
                    if servoDuty==0:
                        servoFlag=1
                p.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)
                
        else:
            print("Device not found!")




        return True
 
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break
