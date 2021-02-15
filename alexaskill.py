import logging
import os
 
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO
 
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)




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




 
SOMETHING = ["something"]
STATUSON = ["on", "switch on", "enable", "power on", "activate", "turn on"] # all values that are defined as synonyms in type
STATUSOFF = ["off", "switch off", "disactivate", "turn off", "disable", "turn off"]
 
@ask.launch
def launch():
    speech_text = 'Welcome to the Raspberry Pi alexa automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)
 
@ask.intent('throwmeIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    if status in SOMETHING:
        GPIO.output(17,GPIO.HIGH)
        return statement('here you go dawlin... catch')
    if status in STATUSON:
        GPIO.output(17,GPIO.HIGH)
        return statement('here you go dawlin... catch')
    if status in STATUSOFF:
        GPIO.output(17,GPIO.HIGH)
        return statement('here you go dawlin... catch')
    else:
        return statement('Sorry, this command is not possible.')
 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)
 
 
@ask.session_ended
def session_ended():
    return "{}", 200
 
 
if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
