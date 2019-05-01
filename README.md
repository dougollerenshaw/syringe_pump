# syringe pump CAD model and control code
source files to build and run a syringe pump

syringe pump model is built in freecad

![Alt text](res/cad_model_image.png?raw=true "CAD model")

Designed to use a Nema 17 stepper motor with an A4988 microstepping driver

Python code communicates with an arduino via USB serial using the PyFirmata package. Arduino controls the stepper driver with digital outputs.

Arduino should have `StandardFirmata` code uploaded (from the arduino IDE: `File > Examples > Firmata > StandardFirmata`)

Arduino wiring and microstepping logic follow the conventions described here:
https://howtomechatronics.com/tutorials/arduino/how-to-control-stepper-motor-with-a4988-driver-and-arduino/

## For remote operation
Pyro4 is used for remote communication

Usage:

On raspberry pi, both a Pyro4 nameserver and the stepper_server must be running

To run nameserver
```
$ conda activate syringe_pump
$ python -m Pyro4.naming -n <IP OF PI>
```

To run stepper_server:
```
$ conda activate syringe_pump
$ python stepper_server.py
```

On remote computer:
```
$ conda activate syringe_pump
```

Then, at a python prompt:
```
>> import Pyro4
>> s = Pyro4.Proxy("PYRONAME:stepper.server")
>> s.calibrate('1ml') #or '5ml'
```

To test remote connection:
```
>> s._pyroBind() # should return True
>> s.toggle_builtin_led() # should toggle the builtin arduino LED
```

To dispense 10 uL:
```
>> s.dispense(10)
```

To retract 100 uL
```
>> s.retract(100)
```
