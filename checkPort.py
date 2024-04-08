import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports()) # search for the devices
for p in ports: 
    print(p)