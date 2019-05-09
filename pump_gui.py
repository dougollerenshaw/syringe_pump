from tkinter import Tk, Label, Button

class SyringePumpGUI:
    def __init__(self, master):
        self.master = master
        master.title("Syringe Pump Remote Control")

        self.label = Label(master, text="Syringe Pump Remote Control")
        self.label.pack()

        self.test_button = Button(master, text="test", command=self.test)
        self.test_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def test(self):
        print("It works!")

root = Tk()
my_gui = SyringePumpGUI(root)
root.mainloop()