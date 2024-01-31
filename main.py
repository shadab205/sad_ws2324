#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import UltrasonicSensor, TouchSensor, GyroSensor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Button, Direction, Color
from pybricks import ev3brick as brick
from pybricks import media
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
max_steer=600
man_arr = [
    man_point(7,   1,   1,     2    ,False),
    man_point(14,  -1,  -1, max_steer,False),
    man_point(15,  -1,   1,     2    ,False),
    man_point( 1,  -1,  -1, max_steer,False),
    man_point(11,  -1,    1, max_steer,False),
    man_point( 5,   1,  -1,max_steer,False),
    man_point( 3,  -1,  1, max_steer,False),
    
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
ev3.speaker.beep()


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
left_button_ctr =0
man=0
man_sample=0

color_sensor = ColorSensor(Port.S3)

lf_cont = pid(200,0,0,200,0.1)
color_feedback = 0

detect_flag = 0


parking_spot_detected = 0;
detect_obj1_flag = 0;
obj1_valid = 0;
obj1_last_distance=0;
start_distance_obj1=0;
obj1_distance=0;
parking_length_detected=0;
park_distance=0;
detect_obj2_flag = 0;
obj2_valid = 0;
obj2_last_distance=0;
start_distance_obj2=0;
obj2_distance=0;

park_flag=0

previous_state='init_0'
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
    
    if (Button.LEFT in b):
        left_button_ctr =left_button_ctr+2
    else:
        if(left_button_ctr>0):
            left_button_ctr=left_button_ctr-1;


    if center_button_ctr>1:
        if sm.current_state == "s_line_follower_mode" and parking_spot_detected == 1:
            sm.receive_input_event("park_begin")
            print("park begin")
            center_button_ctr=0
        else:
            sm.receive_input_event("button_center")
            center_button_ctr=0
#        print("center")
    elif button_press_ctr>5:
        sm.receive_input_event("E_STOP")
        button_press_ctr=0
    elif left_button_ctr>1:
        sm.receive_input_event("button_left")
        left_button_ctr=0
    else:
        sm.receive_input_event("no_event")
    
    color = color_sensor.color()
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
        motor_drive.dc(0)
        motor_turn.dc(0)
            
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
        parking_spot_detected=0
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
        motor_turn.track_target(lf_cont.out)
        motor_drive.run(40)

        if parking_spot_detected==1:
            motor_drive.dc(0)
        else:
            motor_drive.dc(40)  

        distance = sen_us.distance()

        if distance<200 and detect_obj1_flag == 0 and detect_flag==0 and detect_obj2_flag==0 and parking_length_detected ==0:
            start_distance_obj1 = drv.drive_distance_mm;
            detect_obj1_flag = 1;
            obj1_valid = 0;
        
        if detect_obj1_flag == 1:
            obj1_distance = drv.drive_distance_mm - start_distance_obj1
            if obj1_distance > 80:
                obj1_valid = 1
            else:
                obj1_valid = 0;
            
            if distance < 200:
                obj1_last_distance = distance;
        
        if distance >= 200 and detect_flag == 0 and obj1_valid ==1 and detect_obj2_flag==0 and parking_length_detected ==0  :
            start_distance = drv.drive_distance_mm;
            detect_flag = 1;
            parking_length_detected = 0;
            detect_obj1_flag =0 ;
        
        if detect_flag == 1:
            park_distance = drv.drive_distance_mm - start_distance;
            if park_distance > 280 and park_distance < 525:
                parking_length_detected = 1;
            elif park_distance > 525:
                detect_flag = 0;
                parking_length_detected = 0;
            
            #if distance < 200 and park_distance < 425:
            #    detect_flag = 0;
            #    parking_length_detected=0;

        
        if distance <=200 and parking_length_detected == 1 and detect_obj2_flag==0:
            start_distance_obj2 = drv.drive_distance_mm;
            detect_obj2_flag = 1;
            obj2_valid = 0;
            detect_flag=0;
    
        if detect_obj2_flag == 1:
            obj2_distance = drv.drive_distance_mm - start_distance_obj2
            if obj2_distance > 95:
                obj2_valid = 1;
            else:
                obj2_valid = 0;
            
            if distance > 200 :
                detect_obj2_flag = 0
                obj1_valid =0 
                obj2_valid =0
                detect_flag =0
                detect_obj1_flag=0
                parking_length_detected=0
        
        if obj1_valid == 1 and obj2_valid == 1 and parking_length_detected ==1:
            parking_spot_detected =1

    

    elif sm.current_state == "s_semi_auto_mode":
        if Button.LEFT in b and run_flag==False:
            run_flag=True
            man=0
            man_sample=0

        if run_flag==True:
            if man_arr[man].steer_complete==False and man<7:

                if man_arr[man].steer_dir == -1:
                    # if(motor_turn.angle()>-man_arr[man].max_steer_angle):
                    #     motor_turn.dc(50*man_arr[man].steer_dir)
                    # elif(motor_turn.angle()<=-man_arr[man].max_steer_angle):
                    #     man_arr[man].steer_complete=True
                    # else:
                    #     motor_turn.dc(0)
                    motor_turn.track_target((man_arr[man].max_steer_angle*man_arr[man].steer_dir) - 1)
                    if(motor_turn.angle()<=-man_arr[man].max_steer_angle):
                        man_arr[man].steer_complete=True
                        motor_turn.dc(0)
                elif man_arr[man].steer_dir == 1:
                    # if(motor_turn.angle() < man_arr[man].max_steer_angle):
                    #     motor_turn.dc(50*man_arr[man].steer_dir)
                    # elif(motor_turn.angle()>=man_arr[man].max_steer_angle):
                    #     man_arr[man].steer_complete=True
                    # else:
                    #     motor_turn.dc(0)
                    motor_turn.track_target((man_arr[man].max_steer_angle*man_arr[man].steer_dir) + 1)
                    if(motor_turn.angle()>=man_arr[man].max_steer_angle):
                        man_arr[man].steer_complete=True
                        motor_turn.dc(0)
            else:
                motor_turn.dc(0)
            
            if(man_arr[man].steer_complete==True and man<7):
                if(man_sample<=man_arr[man].samples):
                    motor_drive.dc(man_arr[man].drive_dir*max_drive_turn)
                    man_sample=man_sample+1
                elif(man_sample>=man_arr[man].samples):
                    motor_drive.dc(0)
                    man_sample=0
                    man=man+1
                    ev3.speaker.beep()
                else:
                    motor_drive.dc(0)
            else:
                motor_drive.dc(0)

            if man==7:
                run_flag=False

    #print(str(sm.current_state)+','+str(drv.drive_distance_mm) +','+str(drv.drive_distance_mm-start_distance))
    #print(str(sen_us.distance()))
    #print(str(sm.current_state)+','+str(drv.drive_distance_mm)+','+str(sen_us.distance())+','+str(park_distance)+','+str(parking_spot_detected)+','+str(obj1_valid)+','+str(obj2_valid)+','+str(parking_length_detected))
    print(str(sm.current_state)+','+str(drv.drive_distance_mm)+','+str(sen_us.distance())+','+str(park_distance)+','+str(detect_obj1_flag)+','+str(detect_flag)+','+str(detect_obj2_flag)+','+str(parking_length_detected))
    
    ev3.screen.draw_text(5, 50, str(sm.current_state))
    if(previous_state != sm.current_state):
        ev3.speaker.beep()
    
    previous_state=sm.current_state
    wait(100)
    ev3.screen.clear()
