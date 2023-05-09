from microbit import pin0, pin1, pin2, pin3, sleep
from machine import time_pulse_us
import time

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

        if pin3.read_analog() > 800:
            return True
        else:
            return False


def main():
    green_light_delay_ms = 5000
    orange_light_delay_ms = 3000
    red_light_delay_ms = 3000

    current_light = 'red'

    last_ticks = time.ticks_ms()

    while True:
        if current_light == 'red':
            if time.diff_ticks(time.ticks_ms, last_ticks) == red_light_delay_ms:
                Led.green()
                current_light = 'green'
                last_ticks = time.ticks_ms()

            if Sensor.get_presence():
                Radio.send('Trafic.stop:True')

        if current_light == 'green':
            if Sensor.get_presence():
                Radio.send('Trafic.stop:False')

            if time.diff_ticks(time.ticks_ms, last_ticks) == green_light_delay_ms:
                Led.green()
                current_light = 'orange'
                last_ticks = time.ticks_ms()


        if current_light == 'orange':
            if Sensor.get_presence():
                Radio.send('Trafic.stop:True')

            if time.diff_ticks(time.ticks_ms, last_ticks) == orange_light_delay_ms:
                Led.red()
                current_light = 'red'
                last_ticks = time.ticks_ms()




if __name__ == '__main__':
    Led = Led()
    Radio = Radio()
    Sensor = Sensor()

    main()
