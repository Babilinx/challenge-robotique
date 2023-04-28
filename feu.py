from microbit import pin0, pin1, pin2, sleep
from machine import time_pulse_us

from radio import config, send, receive, on


class Led:
    """Handle LEDs"""

    def rgb(self, red: int, green: int, blue: int):
        """Set the color of the LED using RGB values

        Args:
            red (int): Amount of red, from 0 to 255.
            green (int): Amount of green, from 0 to 255.
            blue (int): Amount of blue, from 0 to 255.
        """

        # RGB LED scheme
        #       _______
        #       | | | |
        #       G | | B
        #         | R
        #        GND

        pin0.write_analog(red * 4)
        pin1.write_analog(green * 4)
        pin2.write_analog(blue * 4)

    def green(self):
        self.rgb(0, 0, 0)
        self.rgb(0, 255, 0)

    def orange(self):
        self.rgb(0, 0, 0)
        self.rgb(255, 60, 0)

    def red(self):
        self.rgb(0, 0, 0)
        self.rgb(255, 0, 0)


class Radio:
    """Handle the radio communications with some log prints."""

    def __init__(self, power: int = 7):
        config(channel=6, power=power)
        on()
        print('Radio: Config radio on channel {} and power {}'.format('6', power))

    def send(self, message: str):
        """Send a string threw Bluetooth.

        Args:
            message (str): Message to send.

        Status: Not tested
        """

        send(message)
        print('Radio: Send message {}'.format(message))

    def receive(self) -> str:
        """Return strings that habe been receive threw Bluetooth.

        Returns:
            str: Received message.

        Status: Not tested
        """

        message = receive()
        print('Radio: Recieve {}'.format(message))
        return message


class Sensor:
    """Handle sensors
    """

    def get_distance(self) -> float:
        """Get the distance with the ultrasonic sensor

        Returns:
            float: Distance in centimeters

        Status: Working
        """

        # Send a sound wave
        pin1.write_digital(1)
        sleep(10)
        pin1.write_digital(0)

        pin2.read_digital()
        time = time_pulse_us(pin2, 1)

        distance = 340 * time / 20000

        return distance

    def get_presence(self) -> bool:
        """Get the status of the IR proximity sensor.

        Returns:
            bool: Something detected, or not
        
        Status: In development
        """

        # Do something

        is_presence = True

        return is_presence
