#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import BMP180
import datetime

from time import sleep
from sys import exit

#general needed values
CUTTER_PIN = "P9_12"
TRX_DEVICE = "/dev/ttyO1"
POWER_ON_ALT = 79   #altitude in meters of power on
		    #Mulino airport is officially 79.3
CHUTE_DEPLOY = 300  #altitude to deploy main chute at
MIN_ALT	     = 800  #target minimum altitude before coming back down

#setup the gps and transmitter uart ports
UART.setup("UART1")
UART.setup("UART2")

#open a log file
f_log = open('/home/osu_rocketry/alt_log.out', 'a')

f_log.write("starting a full test\n")

#initialize the cutter pin, it is triggered on a high signal
GPIO.setup(CUTTER_PIN, GPIO.OUT)
GPIO.output(CUTTER_PIN, GPIO.LOW)

#setup gyro and altimeter
alt = BMP180.BMP180(POWER_ON_ALT)

#open a log file
f_log = open('/home/osu_rocketry/alt_log.out', 'a')
f_log.seek(0)
f_log.write("\n")
f_log.write("starting a full test")
gyro = LSM9DS0.LSM9DS0_gyro(LSM9DS0.LSM9DS0_GYRODR_95HZ | LSM9DS0.LSM9DS0_GYRO_CUTOFF_1, LSM9DS0.LSM9DS0_GYROSCALE_200DPS)
accl = LSM9DS0.LSM9DS0_accel()

start_cut = 0
arm_cutter = 0

i = 0

while True:
  try:
    s = str(datetime.datetime.utcnow) + str(i) + "\n"
    f_log.write(s)

    elev_agl = alt.read_agl()
    f_log.write("alt agl")
    f_log.write("\n")
    val = (arm_cutter, start_cut)
    f_log.write(str(elev_agl))
    f_log.write("\n")
    f_log.write(str(val))
    f_log.write("\n")

    (a_x, a_y, a_z) = accel.read_accel()
    f_log.write("accel data")
    f_log.write("\n")
    f_log.write("x " + str(a_x))
    f_log.write("\n")
    f_log.write("y " + str(a_y))
    f_log.write("\n")
    f_log.write("z " + str(a_z))
    f_log.write("\n")

    (g_x, g_y, g_z) = gyro.read()
    f_log.write("gyro data")
    f_log.write("\n")
    f_log.write("x " + str(g_x))
    f_log.write("\n")
    f_log.write("y " + str(g_y))
    f_log.write("\n")
    f_log.write("z " + str(g_z))
    f_log.write("\n")

    f_log.write("temp")
    f_log.write("\n")
    s = str(alt.read_temperature())
    f_log.write(s)
    f_log.write("\n")

    if elev_agl > min_alt:
      arm_cutter = 1
    if arm_cutter and not start_cut:
      if elev_agl <= CHUTE_DEPLOY:
        start_cut = 1
        f_log.write("cutter going to fire")
        f_log.write("\n")
        GPIO.output(CUTTER_PIN, GPIO.HIGH)
        f_log.write("output pin is high, waiting 2 second")
        f_log.write("\n")
        sleep(1) 
        GPIO.output(CUTTER_PIN, GPIO.LOW)
        f_log.write("cutter should have fired")
        f_log.write("\n")
    i += 1
    f_log.write("\n")
    f_log.write("\n")
  except IOError:
    try:
      alt = BMP180.BMP180(POWER_ON_ALT)
      gyro = LSM9DS0.LSM9DS0_gyro(LSM9DS0_GYRODR_95HZ | LSM9DS0_GYRO_CUTOFF_1, LSM9DS0_GYROSCALE_200DPS)
      accl = LSM9DS0.LSM9DS0_accel()
    except:
      f_log.write("sensor errors")
      f_log.write("\n")

exit()
