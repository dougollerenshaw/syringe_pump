from tkinter import Tk, Label, Button
import Pyro4

class SyringePumpGUI:
    def __init__(self, master):
        self.master = master
        master.title("Syringe Pump Remote Control")

        self.pump = Pyro4.Proxy("PYRONAME:stepper.server")
        self.calibrate('3ml')

        self.label = Label(master, text="Syringe Pump Remote Control")
        self.label.pack()

        self.test_button = Button(master, text="test", command=self.test)
        self.test_button.pack()

        self.dispense_button = Button(master, text="dispense 1mL", command=self.dispense(1000))
        self.dispense_button.pack()

        self.retract_button = Button(master, text="retract 1mL", command=self.retract(1000))
        self.retract_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def test(self):
        print("It works!")

root = Tk()
my_gui = SyringePumpGUI(root)
root.mainloop()