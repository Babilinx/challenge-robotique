from microbit import pin1, pin2, pin15, button_b


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
