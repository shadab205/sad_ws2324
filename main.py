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

#variables
start_distance=0
end_distance=0
run_flag=False

while True:

    b = brick.buttons()
    if Button.CENTER in b:
        sm.receive_input_event("button_center")
    else:
        sm.receive_input_event("no_event")
    
    sm.run()
    drv.read_motor_speed_degs(motor_drive.speed())
    drv.interpolate_distance()

    if sm.current_state == "s_init_0":
        pass
    elif sm.current_state == "s_man_mode":

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
        if Button.LEFT in b and run_flag==False:
            start_distance=drv.drive_distance_mm;
            run_flag=True

        if run_flag==True:
                motor_drive.dc(50)
                end_distance=drv.drive_distance_mm;
                if end_distance-start_distance>500:
                    run_flag=False
        else:
            motor_drive.dc(0)
        

    print(str(sm.current_state)+','+str(drv.drive_distance_mm) +','+str(run_flag)+ ','+ str(sen_us.distance())+ ','+str(start_distance)+','+str(end_distance)+','+ str(end_distance-start_distance))
    #print(str(sm.current_state))
    wait(100)