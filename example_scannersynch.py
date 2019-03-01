from pyniexp import scannersynch
from time import sleep

## Initialise
# SSO = scannersynch.scanner_synch()
# SSO = scannersynch.scanner_synch(emul_synch=True)   % emulate scanner synch pulse
# SSO = scannersynch.scanner_synch(emul_buttons=True) % emulate button box
# SSO = scannersynch.scanner_synch(emul_synch=True,emul_buttons=True) % emulate scanner synch pulse and button box


## Example for scanner synch pulse #1: - Simple case
def example_scanner_wait(emul_synch=False):
    SSO = scannersynch.scanner_synch(emul_synch=emul_synch)
    SSO.set_synch_readout_time(0.5)
    SSO.TR = 2
    SSO.start_process()
    
    while SSO.synch_count < 10: # polls 10 pulses
        SSO.wait_for_synch()
        print('[{:.3f}] Pulse {}: {:.3f}. Measured TR = {:.3f}s'.format(
            SSO.clock,
            SSO.synch_count,
            SSO.time_of_last_pulse,
            SSO.measured_TR))

    SSO = None
    
## Example for scanner synch pulse #2 - Background check
def example_scanner_check(emul_synch=False):
    from random import randrange

    SSO = scannersynch.scanner_synch(emul_synch=emul_synch)
    SSO.set_synch_readout_time(0.5)
    SSO.TR = 2
    SSO.start_process()
    
    prevSS = 0
    while SSO.synch_count < 10:         # until 10 pulses
        sleep(randrange(250,350)/1000)  # run code for 250-350 ms ...
        if SSO.synch_count > prevSS:
            print('[{:.3f}] Pulse {}: {:.3f}. Measured TR = {:.3f}s. {} synch pulses has/have been missed'.format(
                SSO.clock,
                SSO.synch_count,
                SSO.time_of_last_pulse,
                SSO.measured_TR,
                SSO.synch_count - prevSS - 1))
            prevSS = SSO.synch_count

    SSO = None

def example_buttons(emul_buttons=False):
    SSO = scannersynch.scanner_synch(emul_buttons=emul_buttons)
    SSO.set_button_readout_time(0.5)    # block individual buttons
    # SSO.set_buttonbox_readout_time(0.5) # block the whole buttonbox
    if emul_buttons: SSO.buttons = ['1','2','3','4']     # emulation Buttons #1-#4 with "1"-"4"
    # SSO.buttonbox_timeout = 1.5;           # Wait for button press for 1.5s
    # SSO.buttonbox_timeout = -1.5;          # Wait for button press for 1.5s even in case of response
    SSO.start_process()

    n = 0
    while n != 10:                   # polls 10 button presses        
        print('\n[{:.3f}s] - Press a button of {}!'.format(SSO.clock,SSO.buttons))
        SSO.wait_for_buttonpress()     # Wait for any button to be pressed
        # SSO.WaitForButtonRelease()   # Wait for any button to be released
        # SSO.WaitForButtonPress(indButton=[2]) # Wait for Button #3 (=zero-indexed 2)
        # SSO.WaitForButtonPress(timeout=2)     # Wait for any button for 2s (overrides SSO.BBoxTimeout only for this event)
        # SSO.WaitForButtonPress(timeout=-2)    # Wait for any (number of) button(s) for 2s even in case of response (overrides SSO.BBoxTimeout only for this event)
        # SSO.WaitForButtonPress(timeout=2,indButton=[2])   # Wait for Button #3 (=zero-indexed 2) for 2s (overrides SSO.BBoxTimeout only for this event)
        # SSO.WaitForButtonPress(timeout=-2,indButton=[2])  # Wait for (any number of presses of) Button #3 (=zero-indexed 2) for 2s even in case of response (overrides SSO.BBoxTimeout only for this event)
        # SSO.WaitForButtonPressInBackground(timeout=-2,indButton=[0,2]); time.sleep(4)   # Wait for any (number of) buttons #1 and #3 (=zero-indexed 0 and 2) for 2s even in case of response (overrides SSO.BBoxTimeout only for this event) in the background
        
        n = n + 1
        for e in range(0,len(SSO.last_events)):
            print('#{} Button {} pressed at {:.3f}s'.format(e,SSO.last_events[e][0],SSO.last_events[e][1]))
        #if emulButtons: print('[{:.3f}s] - Last: Button {} pressed at {:.3f}s'.format(SSO.Clock,[SSO.Keys[i] for i in SSO.LastButtonPress],SSO.TimeOfLastButtonPress))
        #else: print('[{:.3f}s] - Last: Button {} pressed at {:.3f}s'.format(SSO.Clock,SSO.LastButtonPress,SSO.TimeOfLastButtonPress))

    SSO = None

if __name__ == '__main__':
#    example_scanner_wait(False)    
#    example_scanner_check(False)
    example_buttons(True)