class pid:
    def __init__(self,kp,ki,kd,isat,Ts):
        self.kp=kp
        self.ki=ki
        self.kd=kd

        self.iterm=0
        self.pterm=0
        self.dterm=0

        self.out=0
        self.ref=0
        self.fdb=0
        self.error=0

        self.isat=isat
        self.isat_max=isat
        self.isat_min=-isat

        self.Ts=Ts

    def run_pi(self,ref,fdb):
        self.ref=ref
        self.fdb=fdb
        self.error = self.ref-self.fdb

        self.pterm=self.error*self.kp

        self.iterm=self.iterm + (self.error * self.ki * self.Ts)

        if(self.iterm > self.isat_max):
            self.iterm=self.isat_max
        elif(self.iterm < self.isat_min):
            self.iterm=self.isat_min

        self.out=self.pterm+self.iterm+self.dterm

        if(self.out > self.isat_max):
            self.out=self.isat_max
        elif(self.out < self.isat_min):
            self.out=self.isat_min