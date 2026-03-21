from gpiozero import Button
from gpiozero import OutputDevice

sensor = Button(17)
expulsor = OutputDevice(23)

while True:

    if sensor.is_pressed:
        print("Lata detectada")
        expulsor.on()
    else:
        expulsor.off()