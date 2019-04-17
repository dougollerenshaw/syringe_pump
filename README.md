# syringe_pump
source files to build and run a syringe pump

syringe pump model is built in freecad

Designed to use a Nema 17 stepper motor with an A4988 microstepping driver

Python code communicates with an arduino via USB serial using the PyFirmata pacakage. Arduino controls the stepper driver with digital outputs.

Arduino should have `StandardFirmata` code uploaded (from the arduino IDE: `File > Examples > Firmata > StandardFirmata)`

Arduino wiring and microstepping logic follow the conventions described here:
https://howtomechatronics.com/tutorials/arduino/how-to-control-stepper-motor-with-a4988-driver-and-arduino/