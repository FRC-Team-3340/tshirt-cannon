import wpilib

class CannonController:
    
    def __init__(self, pcm_id: int = 0):
        self.compressor = wpilib.Compressor(pcm_id, wpilib.PneumaticsModuleType.CTREPCM)
        # Start disabled so the trigger handles it
        self.compressor.disable()

        # Instantiate 3 independent solenoids (using standard FRC signatures)
        # Note: If your PCM has a non-zero CAN ID, specify it here
        self.barrels = {
            1: wpilib.Solenoid(pcm_id, wpilib.PneumaticsModuleType.CTREPCM, 0),
            2: wpilib.Solenoid(pcm_id, wpilib.PneumaticsModuleType.CTREPCM, 1),
            3: wpilib.Solenoid(pcm_id, wpilib.PneumaticsModuleType.CTREPCM, 2)
        }

        # Safety & pulse tracking timers
        self.hold_timer = wpilib.Timer()
        self.fire_timer = wpilib.Timer()
        
        self.safety_hold_required = 0.5  # Button must be held for 0.5 seconds
        self.pulse_duration = 0.60       # Extended opening duration to dump enough air volume

        # State management
        self.active_barrel_num = None
        self.tracked_barrel_num = None
        self.has_fired_this_press = False

    def set_compressor_state(self, run_compressor: bool):
        if run_compressor:
            self.compressor.enableDigital() # Runs, but obeys the 2-wire limit switch safely
        else:
            self.compressor.disable()

    def update(self, current_target_barrel: int):
        # Active Firing Valve Auto-Shutoff
        if self.active_barrel_num is not None:
            if self.fire_timer.get() >= self.pulse_duration:
                self.barrels[self.active_barrel_num].set(False)
                self.active_barrel_num = None
                self.fire_timer.stop()
            return  # Lock inputs while mid-shot

        # Hold-to-Shoot Logic
        if current_target_barrel > 0:
            if self.tracked_barrel_num != current_target_barrel:
                self.hold_timer.reset()
                self.hold_timer.start()
                self.tracked_barrel_num = current_target_barrel
                self.has_fired_this_press = False
            
            # Button crossed the 0.5s hold safety mark
            if self.hold_timer.get() >= self.safety_hold_required and not self.has_fired_this_press:
                self.execute_fire(self.tracked_barrel_num)
                self.has_fired_this_press = True  
        else:
            # Button released, clear timing blocks
            self.hold_timer.stop()
            self.hold_timer.reset()
            self.tracked_barrel_num = None
            self.has_fired_this_press = False

    def execute_fire(self, barrel_num: int):
        if barrel_num in self.barrels:
            self.active_barrel_num = barrel_num
            self.barrels[barrel_num].set(True)
            self.fire_timer.reset()
            self.fire_timer.start()
