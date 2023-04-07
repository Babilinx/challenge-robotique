from microbit import (
    i2c,
    pin1, pin2, pin13, pin14,
    sleep
)
from machine import time_pulse_us
from radio import (
    config,
    send,
    receive,
    on,
    # off,
)


class Maqueen:
    """Maqueen class for using Maqueen robot"""

    def set_motor(self, motor: str = "all", speed: int = 255, foward: bool = True):
        """Handle motors usage.

        Args:
            motor (str, optional): Select the motor to use. Defaults to "all".
            speed (int, optional): Select the speed of the choosen motor (between 0 and 255). Defaults to 255.
            foward (bool, optional): Select the way that the motos should spin. False to backward. Defaults to True.
        """

        if foward:
            sens = 0x0
        else:
            sens = 0x1

        if motor == "left":
            i2c.write(0x10, bytearray([0x00, sens, speed]))
        elif motor == "right":
            i2c.write(0x10, bytearray([0x02, sens, speed]))
        elif motor == "all":
            i2c.write(0x10, bytearray([0x00, sens, speed]))
            i2c.write(0x10, bytearray([0x02, sens, speed]))

    def get_distance(self) -> float:
        """Get the distance with the ultrasonic sensor

        Returns:
            float: Distance un centimeters
        """

        # Send a sound wave
        pin1.write_digital(1)
        sleep(10)
        pin1.write_digital(0)

        pin2.read_digital()
        time = time_pulse_us(pin2, 1)

        distance = 340 * time / 20000

        return distance

    def get_pratol(self) -> str:
        """Get if one of the two sensors detect the black line.

        Returns:
            str: Tell with sensor was triggered
        """

        if pin13.read_digital():
            return "left"
        if pin14.read_digital():
            return "right"

    def stop(self):
        """Stop all of the motors.
        """

        i2c.write(0x10, bytearray([0x02, 0x0, 0]))
        i2c.write(0x10, bytearray([0x00, 0x0, 0]))


class Radio:
    """Handle the radio communications with some log prints.
    """

    def __init__(self, channel: int,  power: int = 7):
        config(channel=channel, power=power)
        on()
        print("Radio: Config radio on channel {} and power {}".format(channel, power))

    def send(self, message: str):
        """Send a string threw Bluetooth.

        Args:
            message (str): Message to send.
        """

        send(message)
        print("Radio: Send message {}".format(message))

    def receive(self) -> str:
        """Return strings that habe been receive threw Bluetooth.

        Returns:
            str: Received message.
        """

        message = receive()
        print("Radio: Recieve {}".format(message))
        return message
