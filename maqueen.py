from microbit import (i2c, pin1, pin2, pin13, pin14, sleep)
from machine import time_pulse_us
from radio import config, send, receive, on


class Maqueen:
    """Maqueen class for using Maqueen robot"""

    def set_motor(self, motor: str = "all", speed: int = 255):
        """Handle motors usage.

        Args:
            motor (str, optional): Select the motor to use. Defaults to "all".
            speed (int, optional): Select the speed of the choosen motor (between 0 and 255). Defaults to 255.

        Status: Working
        """

        if speed >= 0:
            sens = 0x0
        else:
            sens = 0x1
            speed = -1 * speed

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

    def get_pratol(self) -> str:
        """Get if one of the two sensors detect the black line.

        Returns:
            str: Tell with sensor was triggered

        Status: Working
        """

        if not pin13.read_digital():
            return "left"
        elif not pin14.read_digital():
            return "right"
        else:
            return "none"

    def stop(self):
        """Stop all of the motors.

        Status: Not tested
        """

        i2c.write(0x10, bytearray([0x02, 0x0, 0]))
        i2c.write(0x10, bytearray([0x00, 0x0, 0]))


class Radio:
    """Handle the radio communications with some log prints."""

    def __init__(self, channel: int, power: int = 7):
        config(channel=channel, power=power)
        on()
        print("Radio: Config radio on channel {} and power {}".format(channel, power))

    def send(self, message: str):
        """Send a string threw Bluetooth.

        Args:
            message (str): Message to send.

        Status: Not tested
        """

        send(message)
        print("Radio: Send message {}".format(message))

    def receive(self) -> str:
        """Return strings that habe been receive threw Bluetooth.

        Returns:
            str: Received message.

        Status: Not tested
        """

        message = receive()
        print("Radio: Recieve {}".format(message))
        return message


def joystick_to_mouvement(message_value: str):
    """Make Maqueen move using the joystick on the remote controler.
    """

    value_x, value_y = (value for value in message_value.split('|'))
    value_x, value_y = int(value_x), int(value_y)

    if value_x > 0:
        if value_y > 10:
            Maqueen.set_motor(motor='left', speed=value_y)
            Maqueen.set_motor(motor='right', speed=0)
        elif value_y < -10:
            Maqueen.set_motor(motor='right', speed=-value_y)
            Maqueen.set_motor(motor='left', speed=0)
        else:
            Maqueen.set_motor(speed=value_x)

    elif value_x < 0:
        if value_y > 10:
            Maqueen.set_motor(motor='right', speed=-value_y)
            Maqueen.set_motor(motor='left', speed=0)
        elif value_y < -10:
            Maqueen.set_motor(motor='left', speed=value_y)
            Maqueen.set_motor(motor='right', speed=0)
        else:
            Maqueen.set_motor(speed=value_x)

    elif not value_x and value_y:
        if value_y > 10:
            Maqueen.set_motor(motor='left', speed=value_y)
            Maqueen.set_motor(motor='right', speed=-value_y)
        elif value_y < -10:
            Maqueen.set_motor(motor='right', speed=-value_y)
            Maqueen.set_motor(motor='left', speed=value_y)

    elif not value_x and not value_y:
        Maqueen.stop()


def f_auto_mode():
    stopped = False
    """Follow a black line on white background.
    """
    if Maqueen.get_distance() < 5.0:
        Maqueen.stop()
        stopped = not stopped

    else:
        if stopped:
            Maqueen.set_motor(motor='all', speed=128)
            stopped = not stopped

        patrol = Maqueen.get_pratol()

        if patrol == 'left':
            Maqueen.set_motor(motor='left', speed=30)
            Maqueen.set_motor(motor='right', speed=160)
        elif patrol == 'right':
            Maqueen.set_motor(motor='right', speed=20)
            Maqueen.set_motor(motor='left', speed=160)
        elif patrol == 'none':
            Maqueen.set_motor(motor='all', speed=160)


def main():
    auto_mode = False

    while True:
        message = Radio.receive()
        if message:
            message_type, message_value = message.split(':')

            if message_type == 'Controller.joystick' and not auto_mode:
                joystick_to_mouvement(message_value)

            if message_type == 'Controller.button_b':
                if message_value == 'True':
                    auto_mode = True
                elif message_value == 'False':
                    auto_mode = False

            if message_type == 'Trafic.stop' and auto_mode:
                if message_value == 'True':
                    Maqueen.stop()
                else:
                    f_auto_mode()

        if auto_mode:
            f_auto_mode()



if __name__ == '__main__':
    Radio = Radio(channel=6)
    Maqueen = Maqueen()

    main()
