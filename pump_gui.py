from tkinter import Tk, Label, Button, Entry
import Pyro4

class SyringePumpGUI:
    def __init__(self, master, servername = 'stepper.server', syringe_size='3ml'):
        self.master = master
        self.master.title("Syringe Pump Remote Control")

        self.master.geometry('300x200')

        self.pump = Pyro4.Proxy("PYRONAME:{}".format(servername))
        self.pump.calibrate(syringe_size)

        self.label = Label(self.master, text="Syringe Pump Remote Control")
        self.label.pack()

        self.test_button = Button(self.master, text="test", width=20, command=self.test)
        self.test_button.pack()

        self.dispense_button = Button(self.master, text="dispense 1mL", width=20, command=self.dispense)
        self.dispense_button.pack()

        self.retract_button = Button(self.master, text="retract 1mL", width=20, command=self.retract)
        self.retract_button.pack()

        self.hold_to_retract = Button(self.master, text="hold to retract", width=20, command=self.back_one_step)
        self.hold_to_retract.pack()

        self.dispense_volume_entry =  Entry(self.master, width=20, text="volume in uL")
        self.dispense_volume_entry.pack()

        self.custom_dispense_button = Button(
            self.master, 
            text="Dispense custom volume", 
            width=20, 
            command=self.custom_dispense
            )
        self.custom_dispense_button.pack()

        self.close_button = Button(self.master, text="Close", width=20, command=master.quit)
        self.close_button.pack()

        # self.hold_to_retract.bind('<ButtonPress-1>',self.move_back_continuously('go'))
        # self.hold_to_retract.bind('<ButtonPress-1>',self.move_back_continuously('stop'))

    def test(self):
        print("It works!")

    def move_back_continuously(self,command='go'):
        while command=='go':
            # self.back_one_step()
            pass

    def back_one_step(self):
        print('moving 1 step back')
        self.pump.rotate(steps=1,direction='cw')

    def dispense(self,volume=1000):
        print('dispensing {} ul'.format(volume))
        self.pump.dispense(volume)

    def retract(self,volume=1000):
        print('retracting {} ul'.format(volume))
        self.pump.retract(volume)

    def custom_dispense(self):
        volume = self.dispense_volume_entry.get()
        print('dispensing {} ul'.format(volume))
        self.dispense(int(volume))


    print('in main loop')

root = Tk()
my_gui = SyringePumpGUI(root)
root.mainloop()