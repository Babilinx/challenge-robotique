from microbit import (
    pin0, pin1, pin2
)

from radio import (
    config,
    send,
    receive,
    on,
    # off,
)


class Led:
    """Handle LEDs
    """

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

        pin0.write_analog(red*4)
        pin1.write_analog(green*4)
        pin2.write_analog(blue*4)
