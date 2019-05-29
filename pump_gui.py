from tkinter import Tk, Label, Button, Entry, StringVar
from tkinter import messagebox
import time
import Pyro4

class SyringePumpGUI:
    def __init__(self, master, servername = 'stepper.server', syringe_size='3ml'):
        self.master = master
        self.master.title("Syringe Pump Remote Control")

        self.button_pressed = False
        self.retract_button_pressed = False
        self.dispense_button_pressed = False

        self.retract_limit = None
        self.dispense_limit = None

        self.step_count = StringVar()
        self.total_volume = StringVar()

        self.dispense_direction = 'ccw'
        self.retract_direction = 'cw'
        self.continuous_stepsize = 64 # number of steps to take in each loop when dispensing continuously

        self.master.geometry('300x300')

        self.pump = Pyro4.Proxy("PYRONAME:{}".format(servername))
        # self.pump.calibrate(syringe_size)

        self.label = Label(self.master, text="Syringe Pump Remote Control")
        self.label.pack()

        self.hold_to_dispense = Button(self.master, text="hold to dispense", width=20)
        self.hold_to_dispense.pack()

        self.hold_to_dispense.bind('<ButtonPress-1>',self.start_continuous_dispense)
        self.hold_to_dispense.bind('<ButtonRelease-1>',self.stop_continuous_dispense)

        self.hold_to_retract = Button(self.master, text="hold to retract", width=20)
        self.hold_to_retract.pack()

        self.hold_to_retract.bind('<ButtonPress-1>',self.start_continuous_retract)
        self.hold_to_retract.bind('<ButtonRelease-1>',self.stop_continuous_retract)

        self.flush_cycle = Button(self.master, text='Flush', width=20, command=self.flush)
        self.flush_cycle.pack()
        
        self.dispense_volume_entry =  Entry(self.master, width=20, text="volume in uL")
        self.dispense_volume_entry.pack()

        self.custom_dispense_button = Button(
            self.master, 
            text="Dispense custom volume", 
            width=20, 
            command=self.custom_dispense
            )
        self.custom_dispense_button.pack()

        # self.step_count_display = Label(self.master, width=20, textvariable=self.step_count)
        # self.step_count.set('test test')
        # self.step_count_display.pack()
        self.update_step_count()

        self.update_volume_button = Button(self.master, text="Get updated volume", width=20, command=self.update_step_count)
        self.update_volume_button.pack()

        self.total_volume_display = Label(self.master, width=25, textvariable=self.total_volume)
        self.total_volume.set('test test')
        self.total_volume_display.pack()
        self.update_total_volume()

        self.reset_total_volume_button = Button(self.master, text="reset volume count", width=20, command=self.reset_total_volume)
        self.reset_total_volume_button.pack()

        self.close_button = Button(self.master, text="Close", width=20, command=master.quit)
        self.close_button.pack()


    # ==============================================
    # continuous retract
    # ==============================================
    def start_continuous_retract(self,command):
        self.retract_button_pressed = True
        self.continuous_retract()

    def stop_continuous_retract(self,command):
        self.retract_button_pressed = False

    def continuous_retract(self):
        if self.retract_button_pressed:
            self.pump.rotate(steps=self.continuous_stepsize,direction=self.retract_direction)
            self.master.after(1, self.continuous_retract)
            self.update_step_count()

    # ==============================================
    # continuous dispense
    # ==============================================
    def start_continuous_dispense(self,command):
        self.dispense_button_pressed = True
        self.continuous_dispense()

    def stop_continuous_dispense(self,command):
        self.dispense_button_pressed = False

    def continuous_dispense(self):
        if self.dispense_button_pressed:
            self.pump.rotate(steps=self.continuous_stepsize,direction=self.dispense_direction)
            self.master.after(1, self.continuous_dispense)
            self.update_step_count()

    def flush(self):
        '''fully dispense and refill syringe'''
        confirm = messagebox.askokcancel("About to flush","Syringe must be fully retracted and valves must be in open position. Continue?")
        if confirm:
            self.dispense(volume=3000)
            # overshoot by 100 ul to account for hysteresis in check valves
            self.retract(volume=3100)
            # dispense 100 ul to account for hysteresis in check valves and ensure system is primed
            self.dispense(volume=100)

    def dispense(self,volume=1000):
        print('dispensing {} ul'.format(volume))
        self.pump.dispense(volume)
        self.update_step_count()

    def retract(self,volume=1000):
        print('retracting {} ul'.format(volume))
        self.pump.retract(volume)
        self.update_step_count()

    def custom_dispense(self):
        volume = self.dispense_volume_entry.get()
        print('dispensing {} ul'.format(volume))
        self.dispense(int(volume))

    def update_step_count(self):
        self.step_count.set(self.pump.get_step_count())
        self.update_total_volume()

    def update_total_volume(self):
        self.total_volume.set("Volume dispensed: {} uL".format(
            round(self.pump.get_volume_dispensed(),1)
            ))
        print('total volume is {}'.format(self.pump.get_volume_dispensed()))

    def reset_total_volume(self,value=0):
        self.pump.set_volume_dispensed(0)
        self.update_total_volume()

    print('in main loop')

root = Tk()
my_gui = SyringePumpGUI(root)
root.mainloop()