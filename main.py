#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Button
from pybricks import ev3brick as brick

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
motor_drive = Motor(Port.A)
motor_turn  = Motor(Port.B)
sensor = TouchSensor(Port.S1)
while True:
    b = brick.buttons()
    if Button.LEFT in b:
        motor_turn.dc(-50)

    elif Button.RIGHT in b:
        motor_turn.dc(50)
    else:
        motor_turn.dc(0)

    if sensor.pressed() is True:
        sensor_val = 'True' 
        motor_drive.dc(-50)
    else:
        sensor_val = 'False'
        motor_drive.dc(0)
    print('Speed ' + str(motor_drive.speed()) + ', Angle '+ str(motor_drive.angle())+', Sensor 1 '+ sensor_val)
    wait(100)