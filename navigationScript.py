#!/usr/bin/env python
# Navigational Command Script
import time
import serial
import socket
time.sleep(15)
if __name__ == '__main__':
  isMovingForward = False
  leftMotorSpeed = 0
  rightMotorSpeed = 0
  prevLeftMotorSpeed = 0
  prevRightMotorSpeed = 0
  ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
  )
  ser.write(b'M1: shutdown\r\n')
  ser.write(b'M2: shutdown\r\n')
  classifiedEEG = b'pull'
  s = socket.socket( )
  host = '128.153.182.54'
  port = 12345
  s.bind((host, port))
  s.listen( )
  c, addr = s.accept( )
  print('Got connection from ',addr)
  while True:
    classifiedEEG = c.recv(64)
    c.send(b'You Sent Me A Thingy. Yaaayyyyy.')
    #c.send(b'Direction Received')
    # Set parameters based on classifiedEEG
    if classifiedEEG == b'push' and not isMovingForward: #move forward
      isMovingForward = True
      leftMotorSpeed = 400
      rightMotorSpeed = 375
    elif classifiedEEG == b'left' and isMovingForward: #move forward left
      leftMotorSpeed = 210
      rightMotorSpeed = 450
    elif classifiedEEG == b'left' and not isMovingForward: #rotate left
      leftMotorSpeed = -405
      rightMotorSpeed = 375
    elif classifiedEEG == b'right' and isMovingForward: #move forward right
      leftMotorSpeed = 445
      rightMotorSpeed = 203
    elif classifiedEEG == b'right' and not isMovingForward: #rotate right
      leftMotorSpeed = 405
      rightMotorSpeed = -375
# Send navigationalCommand via Raspberry Pi UART Pins
    if classifiedEEG == b'pull' and (prevLeftMotorSpeed != 0 or prevRightMotorSpeed != 0):
    #stop
      leftStep = int(leftMotorSpeed / 50)
      rightStep = int(rightMotorSpeed / 50)
      for x in range(50):
        leftMotorSpeed = leftMotorSpeed - leftStep
        rightMotorSpeed = rightMotorSpeed - rightStep
        ser.write(b'M1: %d\r\n'%(leftMotorSpeed))
        ser.write(b'M2: %d\r\n'%(rightMotorSpeed))
        time.sleep(0.01)
      leftMotorSpeed = 0
      rightMotorSpeed = 0
      isMovingForward = False
      ser.write(b'M1: shutdown\r\n')
      ser.write(b'M2: shutdown\r\n')
    elif classifiedEEG == b'pull': #stop
      leftMotorSpeed = 0
      rightMotorSpeed = 0
      isMovingForward = False
      ser.write(b'M1: shutdown\r\n')
      ser.write(b'M2: shutdown\r\n')
    else: #move in desired direction from previous direction
      ser.write(b'M1: startup\r\n')
      ser.write(b'M2: startup\r\n')
      leftStep = int((leftMotorSpeed - prevLeftMotorSpeed)/ 50)
      rightStep = int((rightMotorSpeed - prevRightMotorSpeed)/ 50)
      for x in range(50):
        prevLeftMotorSpeed = prevLeftMotorSpeed + leftStep
        prevRightMotorSpeed = prevRightMotorSpeed + rightStep
        ser.write(b'M1: %d\r\n'%(prevLeftMotorSpeed))
        ser.write(b'M2: %d\r\n'%(prevRightMotorSpeed))
        time.sleep(0.01)
    prevLeftMotorSpeed = leftMotorSpeed
    prevRightMotorSpeed = rightMotorSpeed
    print(str(classifiedEEG) + '\n' + str(leftMotorSpeed))
c.close()
