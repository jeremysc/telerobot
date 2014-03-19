#!/usr/bin/env python

"""
Server for driving the create
"""
import socket, sys, urllib2
from irobot import Create
from threading import Timer
from PandaDummy import PandaDummy

CONNECT = '1'
START = '2'
FORWARD = '3'
BACKWARD = '4'
RIGHT = '5'
LEFT = '6'
BRAKE = '7'
SHUTDOWN = '8'
ALLOK = '20'
NOGOOD = '-1'
NOTSTARTED = '-5'

SPEED = 150
TURNSPEED = 100
CHECKDROPTIME = 3 # seconds

def checkDrop(server):
  try:
    response=urllib2.urlopen('http://www.google.com', timeout=2)
    print "Still connected"
    if server.timer:
      server.timer.cancel()
      server.timer = Timer(CHECKDROPTIME, checkDrop, [server])
      server.timer.start()
    return
  except urllib2.URLError as err: pass
  print "Lost connection...resetting"
  server.panda.reset()
  if server.timer:
    server.timer.cancel()
    server.timer = Timer(CHECKDROPTIME, checkDrop, [server])
    server.timer.start()
  return

class Server:
  def __init__(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    self.ip = s.getsockname()[0]

  def go(self, host):
    port = 50000
    backlog = 5
    self.size = 1024
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((host,port))
    self.sock.listen(backlog)
    print "Trying to connect to Panda"
    self.panda = Create(tty="COM3")
    #self.panda = PandaDummy()
    self.started = False
    if self.panda:
      print "Connected to Panda"
      print "Waiting for client on", self.ip
    else:
      print "Problem with Create"
      sys.exit(1)
    
    self.timer = Timer(CHECKDROPTIME, checkDrop, [self])
    self.timer.start()

    while True:
      self.mainLoop()

  def mainLoop(self):
    client, address = self.sock.accept()
    data = client.recv(self.size)
    if data == CONNECT:
      print "Got client"
      client.send(ALLOK)
    elif data == START:
      if self.started:
        print "Reset"
        self.panda.reset()
      else:
        print "Starting"
        self.started = True
        self.panda.start()
      client.send(ALLOK)
    elif data == FORWARD:
      if self.started:
        self.panda.tank(-SPEED,-SPEED)
        client.send(ALLOK)
      else:
        client.send(NOTSTARTED)
    elif data == BACKWARD:
      if self.started:
        self.panda.tank(SPEED,SPEED)
        client.send(ALLOK)
      else:
        client.send(NOTSTARTED)
    elif data == RIGHT:
      if self.started:
        self.panda.right(TURNSPEED)
        client.send(ALLOK)
      else:
        client.send(NOTSTARTED)
    elif data == LEFT:
      if self.started:
        self.panda.left(TURNSPEED)
        client.send(ALLOK)
      else:
        client.send(NOTSTARTED)
    elif data == BRAKE:
      if self.started:
        self.panda.brake()
        client.send(ALLOK)
      else:
        client.send(NOTSTARTED)
    elif data == SHUTDOWN:
      print "Got shutdown...shutting down"
      if self.timer:
        self.timer.cancel()
      self.panda.stop()
      self.started = False
      client.send(ALLOK)
      sys.exit(0)
    else:
      client.send(NOGOOD)
    client.close()

if __name__ == "__main__":
  server = Server()
  try:
    server.go('')
  except KeyboardInterrupt:
    if server.timer:
      server.timer.cancel()

