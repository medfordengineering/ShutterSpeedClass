class PulseSplit:
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
        jmp(pin, "timerstop")    #check if shutter sensor is still sees light
        jmp("timer")
        label("timerstop")      
        mov(isr, invert(x))      
        push()    
 
        
    def __init__(self,pulsePin1, pulsePin2):
        self.sm = PulseSplit.StateMachine(PulseSplit.counter,PulseSplit.pulse_capture,freq=1_000_000, in_base=pulsePin1, jmp_pin=pulsePin2)
        self.sm.active(1)
        PulseSplit.counter += 1
        
    def pulse_split(self):
        if self.sm.rx_fifo() > 0:   #Allow python to check if there is available data
            return self.sm.get() *3
        else:
            return 0
    


