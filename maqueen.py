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
#  off,
  )


class Maqueen:
  """Maqueen class for using Maqueen robot"""

  def set_motor(self, motor: str = "all", speed: int = 255, foward: bool = True):
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
    # Send a sound wave
    pin1.write_digital(1)
    sleep(10)
    pin1.write_digital(0)
    
    pin2.read_digital()
    time = time_pulse_us(pin2, 1)
    
    distance = 340 * time / 20000
    
    return distance
  
  def get_pratol(self) -> str:
    if pin13.read_digital():
      return "left"
    if pin14.read_digital():
      return "right"
  
  def stop(self):
    i2c.write(0x10, bytearray([0x02, 0x0, 0]))
    i2c.write(0x10, bytearray([0x00, 0x0, 0]))

class Radio:

  def __init__(self, channel: int,  power: int = 7):
    config(channel=channel, power=power)
    on()
    print("Radio: Config radio on channel {} and power {}".format(channel, power))
  
  def send(self, message: str):
    send(message)
    print("Radio: Send message {}".format(message))

  def receive(self) -> str:
    message = receive()
    print("Radio: Recieve {}".format(message))
    return message