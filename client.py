#!/usr/bin/env python

"""
Client for driving the create
"""
import socket, sys, Tkinter, time
from threading import Timer

CONNECT = '1'
START = '2'
FORWARD = '3'
BACKWARD = '4'
RIGHT = '5'
LEFT = '6'
BRAKE = '7'
SHUTDOWN = '8'
RESET = '9'
ALLOK = '20'
NOGOOD = '-1'
NOTSTARTED = '-5'

commands = {
  'i': [START, "START"],
  'w': [FORWARD, "FORWARD"],
  'a': [LEFT, "LEFT"],
  's': [BACKWARD, "BACKWARD"],
  'd': [RIGHT, "RIGHT"],
  'k': [SHUTDOWN, "SHUTDOWN"] }

def release(tk):
  c = tk.down
  tk.down = None
  tk.key_rel(c)

class Driver:
  def __init__(self):
    return
  
  def go(self, host):
    self.host = host
    self.root = Tkinter.Tk()
    prompt = 'i to start, k to shutdown'
    self.label1 = Tkinter.Label(self.root, text=prompt, width=len(prompt), bg='yellow')
    self.label1.pack()
    self.root.bind_all('<KeyPress>', self.key_press)
    self.root.bind_all('<KeyRelease>', self.key_release)
    self.timer = None
    self.down = None
    self.connected = False
    self.connect()

    self.root.mainloop()
  
  def connect(self):
    self.connected = False
    while True:
      port = 50000
      size = 1024
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(3)
      try:
        sock.connect((self.host,port))
        sock.send(CONNECT)
        data = sock.recv(size)
        sock.close()
        if data == ALLOK:
          self.connected = True
          print "Connected to %s" % self.host
          self.label1.config(text="Connected to %s" % self.host)
          return
        else:
          print "Trouble connecting to %s" % self.host
          print "trying again..."
          time.sleep(3)
      except:
        print "Trouble connecting to %s" % self.host
        print "trying again..."
        time.sleep(3)

  def reconnect(self):
    self.label1.config(text="Reconnecting")
    print "Reconnecting"
    self.connect()
    self.send(BRAKE)

  def send(self, command):
    port = 50000
    size = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
      sock.connect((self.host,port))
      sock.send(command)
      data = sock.recv(size)
      sock.close()
      return data
    except:
      self.connected = False
      print "Problem sending"
      self.label1.config(text="Reconnecting")
      self.reconnect()
      return ALLOK
  
  def isDown(self, char):
    return (self.down == char)

  def releaseTimer(self):
    if self.timer:
      self.timer.cancel()
    self.timer = Timer(0.1, release, [self])
    self.timer.start()

  # THIS IS WHERE I PUT THE RAISINS INTO THE DOUGH
  def key_press(self, event):
    if not self.connected:
      self.revert()
      return
    if event.char == event.keysym:
      if (event.char not in commands):
        return
      if self.isDown(event.char):
        return
      self.down = event.char
      command, name = commands[event.char]
      stat = self.send(command)
      if (command == SHUTDOWN) and stat == ALLOK:
        sys.exit(0)
      elif stat == ALLOK:
        self.label1.config(text="SUCCESS: " + name)
      elif stat == NOTSTARTED:
        self.label1.config(text="NOT STARTED, PRESS i")
      else:
        self.label1.config(text="ERROR: " + name)
  
  def key_release(self, event):
    if not self.connected:
      self.revert()
      return
    if event.char == event.keysym:
      if (event.char not in commands):
        return
      if self.isDown(event.char):
        self.releaseTimer()
        return
      command, name = commands[event.char]
      if (command in [FORWARD, BACKWARD, RIGHT, LEFT]):
        stat = self.send(BRAKE)
        if stat == ALLOK:
          self.label1.config(text="BRAKING")
        elif stat == NOTSTARTED:
          self.label1.config(text="NOT STARTED, PRESS i")
        else:
          self.label1.config(text="ERROR: BRAKING")
  
  def revert(self):
    self.down = None
    self.connected = False
    if self.timer:
      self.timer.cancel()

  def key_rel(self, char):
    if not self.connected:
      self.revert()
      return
    if (char not in commands):
      return
    command, name = commands[char]
    if (command in [FORWARD, BACKWARD, RIGHT, LEFT]):
      stat = self.send(BRAKE)
      if stat == ALLOK:
        self.label1.config(text="BRAKING")
      elif stat == NOTSTARTED:
        self.label1.config(text="NOT STARTED, PRESS i")
      else:
        self.label1.config(text="ERROR: BRAKING")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Pass in Server IP Address!"
    sys.exit(0)
  ip = sys.argv[1]
  driver = Driver()
  try:
    driver.go(ip)
  except KeyboardInterrupt:
    if driver.timer:
      driver.timer.cancel()
    if driver.root:
      driver.root.quit()
      driver.root.destroy()
    sys.exit(0)
