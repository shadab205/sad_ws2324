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

while True:
    b = brick.buttons()
    if Button.UP in b:
        motor_turn.dc(-50)

    elif Button.DOWN in b:
        motor_turn.dc(50)
    else:
        motor_turn.dc(0)

    if Button.LEFT in b:
                motor_drive.dc(50)
    elif Button.RIGHT in b:
        motor_drive.dc(-30)
    else:
        motor_drive.dc(0)
    print('Speed ' + str(motor_drive.speed()) + ', Angle '+ str(motor_drive.angle()))
    wait(100)