from microbit import pin0, pin1, pin2

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
        #       R | | B
        #         | G
        #        GND

        pin0.write_analog(red * 4)
        pin1.write_analog(green * 4)
        pin2.write_analog(blue * 4)


class Radio:
    """Handle the radio communications with some log prints."""

    def __init__(self, channel: int, power: int = 7):
        config(channel=channel, power=power)
        on()
        print('Radio: Config radio on channel {} and power {}'.format(channel, power))

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
