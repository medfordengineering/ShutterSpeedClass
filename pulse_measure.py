class PulseWidth:
    from rp2 import PIO, StateMachine, asm_pio
    from machine import Pin
    counter=0
    @asm_pio()
    def pulse_capture():
        
        mov(x, invert(null)) #move the full monty-32bits to the x register
        wait(1, pin, 0)      #wait for shutter sensor to see light
        label("timer")
        jmp(x_dec, "test")   #subtract one from x register
        jmp ("timerstop")    #fail safe if shutter sensor remains on
        label("test")
        jmp(pin, "timer")    #check if shutter sensor is still sees light
        label("timerstop")      
        mov(isr, invert(x))      
        push()    
        
    def __init__(self,pulsePin):
        self.sm = PulseWidth.StateMachine(PulseWidth.counter,PulseWidth.pulse_capture,freq=1_000_000, in_base=pulsePin, jmp_pin=pulsePin)
        self.sm.active(1)
        PulseWidth.counter += 1
        
    def pulse_width(self):
        if self.sm.rx_fifo() > 0:   #Allow python to check if there is available data
            return self.sm.get() *2
        else:
            return 0
    


    