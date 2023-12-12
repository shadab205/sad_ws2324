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
steer_pi = pid(1,0,0,50,0.1)

if two_motors == True:
    motor_turn  = Motor(Port.B)
print("Rover_distance, Sensor_distance")

#variables
start_distance=0
end_distance=0
run_flag=False
steer_angle=0

while True:

    b = brick.buttons()

    if Button.CENTER in b:
        sm.receive_input_event("button_center")
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
    elif sm.current_state == "s_semi_auto_mode":
        if Button.LEFT in b and run_flag==False:
            start_distance=drv.drive_distance_mm;
            run_flag=True

        if run_flag==True:
               
            motor_drive.dc(30)

            steer_pi.run_pi(0,steer_angle)
            if(motor_turn.angle()>360 && -steer_pi.out>0):
                motor_turn.dc(-steer_pi.out)
            elif(motor_turn.angle()<-360 && -steer_pi.out<0):
                motor_turn.dc(-steer_pi.out)
            #elif(motor_turn.angle()>360):
            #    motor_turn.dc(-10)
            #elif(motor_turn.angle()<-360):
            #    motor_turn.dc(10)                
            #motor_turn.track_target(steer_pi.out)
            end_distance=drv.drive_distance_mm;

            if end_distance-start_distance>800:
                run_flag=False
        else:
            motor_drive.dc(0)
        

    #print(str(sm.current_state)+','+str(drv.drive_distance_mm) +','+str(run_flag)+ ','+ str(sen_us.distance())+ ','+str(start_distance)+','+str(end_distance)+','+ str(end_distance-start_distance))
    #print(str(sm.current_state))
    print(str(sm.current_state)+','+str(drv.theta)+','+str(motor_turn.angle())+','+str(steer_pi.ref)+','+str(steer_pi.fdb)+','+str(steer_pi.error)+','+str(steer_pi.out))
    wait(100)