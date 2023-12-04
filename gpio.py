import RPi.GPIO as GPIO

import asyncio

GPIO.setmode(GPIO.BCM)
output_pin_bibi = 4
GPIO.setup(output_pin_bibi, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(output_pin_bibi, GPIO.LOW)


# MARK: GPIO Functions
def push_down_bibi_button():
    GPIO.output(output_pin_bibi, GPIO.HIGH)

def release_bibi_button():
    GPIO.output(output_pin_bibi, GPIO.LOW)

async def tap_bibi_button():
    push_down_bibi_button()
    await asyncio.sleep(0.1)
    release_bibi_button()

def bibi_yellow_alarm_action():
    #actions here
    print('bibi yellow triggered')
    asyncio.run(tap_bibi_button())

def bibi_red_alarm_action():
    #actions here
    print('bibi red triggered')
    asyncio.run(tap_bibi_button())