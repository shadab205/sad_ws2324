#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
motor = Motor(Port.A)
sensor = TouchSensor(Port.S1)
while True:
    if sensor.pressed() is True:
        sensor_val = 'True' 
        motor.dc(50)
    else:
        sensor_val = 'False'
        motor.dc(0)
    print('Speed ' + str(motor.speed()) + ', Angle '+ str(motor.angle())+', Sensor 1 '+ sensor_val)
    wait(100)