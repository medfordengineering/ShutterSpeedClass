class FirstCurtain:
    from rp2 import PIO, StateMachine, asm_pio
    from machine import Pin
    
    @asm_pio()
    def pulse_capture():

        mov(x, invert(null))     #move the full monty-32bits to the x register
        wait(1, pin, 0)          #wait for first pulse to go high
        
        label("timer")
        jmp(x_dec, "test")       #subtract one from x register and goto test 1 CYCLE
        jmp ("timerstop")        #else if x register reaches zero leave method
        label("test")
        jmp(pin, "timerstop")    #if second pulse is high stop counting      1 CYCLE
        jmp("timer")             #else if go back to counting down           1 CYCLE
        label("timerstop")      
        mov(isr, invert(x))      
        push()    
        
    def __init__(self,sm_id, pulsePin1, pulsePin2):
        self.sm = FirstCurtain.StateMachine(sm_id,FirstCurtain.pulse_capture,freq=1_000_000, in_base=pulsePin1, jmp_pin=pulsePin2)
        self.sm.active(1)
        
    def curtain_speed(self):
        if self.sm.rx_fifo() > 0:   #Allow python to check if there is available data
            return self.sm.get() *3
        else:
            return 0
    

