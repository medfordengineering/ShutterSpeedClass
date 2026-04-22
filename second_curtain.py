class SecondCurtain:
    from rp2 import PIO, StateMachine, asm_pio
    from machine import Pin
    @asm_pio()
    def pulse_capture():

        mov(x, invert(null)) #move the full monty-32bits to the x register
        wait(1, pin, 0)      #wait while first pulse low
        wait(0, pin, 0)      #wait for first pulse to go low
        
        label("sync")
        jmp(pin, "timer")     #if second pulse high goto timer       1 CYCLE
        jmp(x_dec, "sync")    #if second pulse low keep counting     1 CYCLE
        
        label("timer")
        jmp(x_dec, "test")   #subtract one from x register           1 CYCLE
        jmp ("timerstop")    #leave method if x register gets to zero 
        label("test")
        jmp(pin, "timer")    #check if second pulse high keep counting 1 CYCLE
        label("timerstop")      
        mov(isr, invert(x))      
        push()    
 
    def __init__(self,sm_id, pulsePin1, pulsePin2):
        self.sm = SecondCurtain.StateMachine(sm_id,SecondCurtain.pulse_capture,freq=1_000_000, in_base=pulsePin1, jmp_pin=pulsePin2)
        self.sm.active(1)
        
    def curtain_speed(self):
        if self.sm.rx_fifo() > 0:   #Allow python to check if there is available data
            return self.sm.get() *2
        else:
            return 0
    