#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import TouchSensor
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Button
from pybricks import ev3brick as brick
import math

# State machine init start

from state_machine import StateMachine
from drive import Drive

b = brick.buttons()
sm = StateMachine()
drv= Drive()
# State machine init end

two_motors = True
# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
motor_drive = Motor(Port.A)

#init sensor
sen_us=UltrasonicSensor(Port.S1)

if two_motors == True:
    motor_turn  = Motor(Port.B)
print("Rover_distance, Sensor_distance")

while True:

    b = brick.buttons()
    if Button.CENTER in b:
        sm.receive_input_event("button_center")
    else:
        sm.receive_input_event("no_event")
    
    sm.run()

    if sm.current_state == "s_init_0":
        pass
    elif sm.current_state == "s_man_mode":
        drv.read_motor_speed_degs(motor_drive.speed())
        drv.interpolate_distance()
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
                            
    elif sm.current_state == "s_semi_auto_mode":
        if Button.UP in b:
            start_distance=drv.drive_distance_mm;
            while(start_distance-end_distance<=500):
                motor_drive.dc(10)
                end_distance=drv.drive_distance_mm;
        

    print(str(drv.drive_distance_mm) + ','+ str(sen_us.distance()))
    wait(100)