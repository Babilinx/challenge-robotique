from microbit import pin1, pin2, pin15, button_b, sleep, display, Image
from radio import config, send, receive, on


class Controler:
    """Handle the wireless controler."""

    def get_analog_joystick_x(self) -> int:
        return pin1.read_analog()

    def get_analog_joystick_y(self) -> int:
        return pin2.read_analog()

    def convert_joystick_to_motor(self, value: int) -> int:
        if value == 525:
            return 0
        if value > 525:
            return int((value - 525) / (29 / 15))
        if value < 525:
            return int((493 - value) / (29 / 15))

    def get_red_button(self) -> bool:
        return pin15.read_digital()

    def get_button_B(self) -> bool:
        return button_b.is_pressed()

    def show_auto_mode(self, status):
        if status == 'True':
            display.show(Image('00000:'
                               '00000:'
                               '00009:'
                               '00000:'
                               '00000:'))

        if status == 'False':
            display.clear()


class Radio:
    """Handle the radio communications with some log prints."""

    def __init__(self, power: int = 7):
        config(channel=6, power=power)
        on()
        print("Radio: Config radio on channel {} and power {}".format("6", power))

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


def main():
    button_b_status = 'False'

    while True:
        # Get data
        analog_joystick_x = Controler.get_analog_joystick_x()
        analog_joystick_y = Controler.get_analog_joystick_y()

        joystick_x = Controler.convert_joystick_to_motor(analog_joystick_x)
        joystick_y = Controler.convert_joystick_to_motor(analog_joystick_y)

        button_b = Controler.get_button_B()
        red_button = Controler.get_red_button()

        if joystick_x <= 10 and joystick_x >= -10: joystick_x = 0
        if joystick_y <= 10 and joystick_y >= -10: joystick_y = 0
        if joystick_x > 255: joystick_x = 255
        if joystick_x < -255: joystick_x = -255
        if joystick_y > 255: joystick_y = 255
        if joystick_y < -254: joystick_y = -255

        # Toggle for button B
        if button_b and button_b_status == 'False':
            button_b_status = 'True'
            sleep(200)
        elif button_b and button_b_status == 'True':
            button_b_status = 'False'
            sleep(200)

        Controler.show_auto_mode(button_b_status)

        # Send Data to Maqueen
        Radio.send("Controller.joystick:{}|{}".format(joystick_y, joystick_x))
        Radio.send("Controller.button_b:{}".format(button_b))
        Radio.send("Controller.red_button:{}".format(red_button))

        sleep(1 / 30)


if __name__ == "__main__":
    Radio = Radio()
    Controler = Controler()

    main()
