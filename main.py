#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import UltrasonicSensor, TouchSensor, GyroSensor, ColorSensor
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

class man_point:
    def __init__(self, x, y, z, phi, condition):
        self.samples = x
        self.drive_dir = y
        self.steer_dir = z
        self.max_steer_angle = phi
        self.steer_complete = condition


# Creating an array of Point objects
max_steer=650
man_arr = [
    man_point(10,  1,  1, 1, False),
    man_point(37, -1,  1, max_steer,False),
    man_point(13, -1, -1, max_steer,False),
    man_point(7,   1,  1, max_steer,False),
    man_point(8,  -1, -1, max_steer,False),
    man_point(4,   1,  1, max_steer,False),
    man_point(4,  -1, -1, 1,False),
]
# PI controller init

max_steer=650
max_drive_turn=40
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
man=0
man_sample=0

color_sensor = ColorSensor(Port.S3)

lf_cont = pid(200,0,0,200,0.1)
color_feedback = 0

detect_flag = False
parking_spot_detected = False

while True:

    c = emergency_button.pressed()
    if (c == True):
        button_press_ctr = button_press_ctr+2 
    else:
        if(button_press_ctr>0):
            button_press_ctr=button_press_ctr-1
    
    b = brick.buttons()
    if (Button.CENTER in b):
        center_button_ctr = center_button_ctr+2 
    else:
        if(center_button_ctr>0):
            center_button_ctr=center_button_ctr-1

    if center_button_ctr>1:
        if sm.current_state == "s_line_follower_mode" and parking_spot_detected = True:
            sm.receive_input_event("park_brgin")
        else:
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
            motor_drive.dc(30)
        elif Button.RIGHT in b:
            motor_drive.dc(-30)
        else:
            motor_drive.dc(0)
    elif sm.current_state == "s_pre_semi_auto_mode":
        motor_turn.reset_angle(0)
        steer_pi.out=0
        steer_pi.ref=0
        steer_pi.fdb=0
        for man_var in man_arr:
            man_var.steer_complete=False
    elif sm.current_state == "s_line_follower_mode":
        color = color_sensor.color()   
       
        if  color== Color.RED:
            color_feedback=-1
        elif color == Color.BLACK:
            color_feedback = 0
        elif color == Color.WHITE:
            color_feedback = 1

        lf_cont.run_pi(0, color_feedback)
        steer_motor.track_target(lf_cont.out)
        drive_motor.run(100)

        if parking_spot_detected==True:
            drive_motor.dc(0)
        else:
            drive_motor.dc(50)  

        distance = ultra_sensor.distance()

        if distance > 200 and detect_flag == False:
            start_distance = drv.drive_distance_mm
            detect_flag = True
            parking_spot_detected = False
        if detect_flag == True:
            park_distance = drv.drive_distance_mm - start_distance
            if park_distance > 300:
                parking_spot_detected = True
            else :
                parking_spot_detected = False
            if distance < 200:
                detect_flag = False

    elif sm.current_state == "s_semi_auto_mode":
        if Button.LEFT in b and run_flag==False:
            run_flag=True
            man=0
            man_sample=0

        if run_flag==True:
            if man_arr[man].steer_complete==False and man<6:
                if man_arr[man].steer_dir == -1:
                    if(motor_turn.angle()>-man_arr[man].max_steer_angle):
                        motor_turn.dc(50*man_arr[man].steer_dir)
                    elif(motor_turn.angle()<=-man_arr[man].max_steer_angle):
                        man_arr[man].steer_complete=True
                    else:
                        motor_turn.dc(0)
                elif man_arr[man].steer_dir == 1:
                    if(motor_turn.angle() < man_arr[man].max_steer_angle):
                        motor_turn.dc(50*man_arr[man].steer_dir)
                    elif(motor_turn.angle()>=man_arr[man].max_steer_angle):
                        man_arr[man].steer_complete=True
                    else:
                        motor_turn.dc(0)
            else:
                motor_turn.dc(0)
            
            if(man_arr[man].steer_complete==True and man<6):
                if(man_sample<=man_arr[man].samples):
                    motor_drive.dc(man_arr[man].drive_dir*max_drive_turn)
                    man_sample=man_sample+1
                elif(man_sample>=man_arr[man].samples):
                    motor_drive.dc(0)
                    man_sample=0
                    man=man+1
                else:
                    motor_drive.dc(0)
            else:
                motor_drive.dc(0)

            if man==6:
                run_flag=False

    #print(str(sm.current_state)+','+str(drv.drive_distance_mm) +','+str(drv.drive_distance_mm-start_distance))
    #print(str(sm.current_state))
    print(str(sm.current_state)+','+str(drv.theta)+','+str(motor_turn.angle())+','+str(man)+','+str(man_sample))
    wait(100)
