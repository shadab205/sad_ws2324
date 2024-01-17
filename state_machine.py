class StateMachine:
    def __init__(self):
        self.states = ["s_init_0", "s_man_mode", "s_semi_auto_mode","s_pre_semi_auto_mode","s_line_follower_mode"]
        self.transitions = [
            {"current_state": "s_init_0", "event": "button_center", "next_state": "s_man_mode"},
            {"current_state": "s_man_mode", "event": "button_center", "next_state": "s_pre_semi_auto_mode"},
            {"current_state": "s_pre_semi_auto_mode", "event": "button_center", "next_state": "s_line_follower_mode"},
            {"current_state": "s_line_follower_mode", "event": "park_begin", "next_state": "s_semi_auto_mode"},
            {"current_state": "s_semi_auto_mode", "event": "E_STOP", "next_state": "s_man_mode"},
            

            {"current_state": "s_init_0", "event": "E_STOP", "next_state": "s_init_0"},
            {"current_state": "s_man_mode", "event": "E_STOP", "next_state": "s_init_0"},
            ##{"current_state": "s_semi_auto_mode", "event": "E_STOP", "next_state": "s_init_0"},
            {"current_state": "s_pre_semi_auto_mode", "event": "E_STOP", "next_state": "s_init_0"},
            {"current_state": "s_line_follower_mode", "event": "E_STOP", "next_state": "s_init_0"}
            ]
        self.events = ["button_center","button_left","button_right","no_event","E_STOP","park_begin"]
        self.current_state = self.states[0]
        self.is_running = True
        self.input_event = "no_event"
        
    def transition(self, event):
        for t in self.transitions:
            if t["current_state"] == self.current_state and t["event"] == event:
                self.current_state = t["next_state"]
                return True
        return False

    def run(self):
        #while self.is_running:
        #print("-----------------------------------------")
        #print("Current state:" + str(self.current_state))

        event = self.get_valid_event()
        #print("event="+event)
        if not self.transition(event):
            pass
            #print("Invalid event. No transition occurred.")
            
        self.is_running = self.check_termination_condition()
        pass
        #print("-----------------------------------------")    
    def get_valid_event(self):
        while True:
            parsed_event = self.input_event
            #print("parsed_event="+parsed_event)
            if parsed_event is not None:
                return parsed_event
            else:
                return "no_event"

    def check_termination_condition(self):
        return True
    
    def s_init_0_operation():
        pass
        #print("Performing init_0 operation")

    def s_man_mode_operation():
        pass
        #print("Performing man_mode operation")
        
    def receive_input_event(self,user_input):
        self.input_event=user_input
        #print("User input="+self.input_event)
