Client and server for the iRobot Create



0. Install Python 2.7: http://python.org/ftp/python/2.7.2/python-2.7.2.msi



On the netbook connected to the Create:

1. Turn on the Create and connect it to the netbook.

2. Click the start menu and type 'cmd' to get a command prompt

3. Navigate to this folder

4. Run: C:\Python27\python.exe server.py

5. Note the IP address of the netbook, where it says "Waiting for client on..."



On the other laptop:

1. Click the start menu and type 'cmd' to get a command prompt

2. Navigate to this folder

3. Run: C:\Python27\python.exe client.py 18.189.105.225

	replacing 18.189.105.225 with the netbook IP address

4. Press 'i' to start, wasd to move, and 'k' to shutdown

