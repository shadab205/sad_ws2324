#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import TouchSensor, GyroSensor
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Button, Direction
from pybricks import ev3brick as brick
import math
from pid_controller import pid
# State machine init start

from state_machine import StateMachine
from drive import Drive

# PI controller init


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
sen_us = UltrasonicSensor(Port.S1)
sen_gyro = GyroSensor(Port.S2,Direction.CLOCKWISE)

#init_pi
steer_pi = pid(2.5,0,0,70,0.1)

if two_motors == True:
    motor_turn  = Motor(Port.B)
print("Rover_distance, Sensor_distance")

#touchsensor
emergency_button=TouchSensor(Port.S4)

#variables
start_distance=0
end_distance=0
run_flag=False
steer_angle=0
turn_command=0

button_press_ctr = 0
center_button_ctr =0

while True:

    c = emergency_button.pressed()
    if (c == True):
        button_press_ctr = button_press_ctr+1 
    else:
        if(button_press_ctr>0):
            button_press_ctr=button_press_ctr-1
    
    b = brick.buttons()
    if (Button.CENTER in b):
        center_button_ctr = center_button_ctr+1 
    else:
        if(center_button_ctr>0):
            center_button_ctr=center_button_ctr-1

    if center_button_ctr>1:
        sm.receive_input_event("button_center")
#        print("center")
    elif button_press_ctr>5:
        sm.receive_input_event("E_STOP")
        button_press_ctr=0
    else:
        sm.receive_input_event("no_event")
    
    sm.run()

    drv.read_motor_speed_degs(motor_drive.speed())
    drv.interpolate_distance()
    drv.get_theta(sen_gyro.angle())
    drv.calc_coordinates()
    steer_angle = drv.theta;

    b = brick.buttons()
    if sm.current_state == "s_init_0":
        sen_gyro.reset_angle(0)
        drv.xc=0
        drv.yc=0
        drv.theta=0
        motor_turn.reset_angle(0)
            
    elif sm.current_state == "s_man_mode":

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
    elif sm.current_state == "s_pre_semi_auto_mode":
        motor_turn.reset_angle(0)
        steer_pi.out=0
        steer_pi.ref=0
        steer_pi.fdb=0
    elif sm.current_state == "s_semi_auto_mode":
        if Button.LEFT in b and run_flag==False:
            start_distance=drv.drive_distance_mm;
            run_flag=True

        if run_flag==True:
               
            motor_drive.dc(50)

            steer_pi.run_pi(0,steer_angle)
            turn_command=-steer_pi.out

#            if(motor_turn.angle()>500 and turn_command<0):
#                motor_turn.dc(turn_command)
#            elif(motor_turn.angle()<-500 and turn_command>0):
#                motor_turn.dc(turn_command)
#            else:
#                motor_turn.dc(0)

#            if(motor_turn.angle()<360 and motor_turn.angle()>-360):
#                 motor_turn.dc(turn_command)  
            if(motor_turn.angle()>500):  
                turn_command=turn_command-30
            elif(motor_turn.angle()<-500):  
                turn_command=turn_command+30
                
            motor_turn.dc(turn_command)                  
            end_distance=drv.drive_distance_mm;

            if end_distance-start_distance>800:
                run_flag=False
        else:
            motor_drive.dc(0)
            motor_turn.dc(0)
        

    #print(str(sm.current_state)+','+str(drv.drive_distance_mm) +','+str(run_flag)+ ','+ str(sen_us.distance())+ ','+str(start_distance)+','+str(end_distance)+','+ str(end_distance-start_distance))
    #print(str(sm.current_state))
    print(str(sm.current_state)+','+str(drv.theta)+','+str(motor_turn.angle())+','+str(steer_pi.ref)+','+str(steer_pi.fdb)+','+str(steer_pi.error)+','+str(turn_command))
    wait(100)