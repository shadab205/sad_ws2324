import math
class Drive:
    def __init__(self):
        self.drive_distance_mm=0
        self.drive_speed_mmps=0
        self.drive_speed_rps=0
        self.drive_speed_degs=0
        self.lego_wheel_circumference_mm=172.7
        self.Ts=0.1
        self.xc=0
        self.yc=0
        self.theta=0
        
    def read_motor_speed_degs(self,motor_speed_degs):
        self.drive_speed_degs=motor_speed_degs
    
    def calc_speed_rps(self):
        self.drive_speed_rps=self.drive_speed_degs/360.0
        
    def calc_speed_mmps(self):
        self.drive_speed_mmps=self.drive_speed_rps*self.lego_wheel_circumference_mm
    
    def interpolate_distance(self):
        self.calc_speed_rps()
        self.calc_speed_mmps()
        self.drive_distance_mm=self.drive_distance_mm+(self.drive_speed_mmps*self.Ts)
        
    def get_theta(self, input_theta):
        self.theta=input_theta

    def calc_coordinates(self):
        self.xc=self.xc+(self.drive_speed_mmps*self.Ts*math.cos(self.theta))
        self.yc=self.xc+(self.drive_speed_mmps*self.Ts*math.sin(self.theta))
