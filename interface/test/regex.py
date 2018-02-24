import re
import serial.tools.list_ports

seq = re.compile(r'COM[0-9]')
if 'Arduino' in portString:
    port = seq.match(portString).group()
else :
    port = None
print(port)