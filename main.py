#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Button
from pybricks import ev3brick as brick
import math

# State machine init start

from state_machine import StateMachine


b = brick.buttons()
sm = StateMachine()

# State machine init end

two_motors = False
# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
motor_drive = Motor(Port.A)

if two_motors == True:
    motor_turn  = Motor(Port.B)

while True:

    b = brick.buttons()
    if Button.CENTER in b:
        sm.receive_input_event("button_center")
    else:
        sm.receive_input_event("no_event")
    sm.run()
    if sm.current_state == "s_init_0":
        print("we are in init")
    elif sm.current_state == "s_man_mode":
        print("we are in man_mode")
    wait(1000)
'''
while True:
    b = brick.buttons()
    if two_motors == True:
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
'''