#! /usr/bin/env python
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from subprocess import Popen, PIPE
import time
import os

#default values
Volt=0
Ampere=0
PowerFactor=0
filename = "alternatives/default_energy.txt"

#read data of PDU via snmp and bash tool snmpget
def getSNMP(IP, OID):
	process = Popen("snmpget -v1 -c private "+str(IP)+" "+str(OID),stdout=PIPE, shell=True)
	while True:
		line=process.stdout.readline().rstrip()
		if not line:
			break

		line=str(line).split(":")
		file.write(","+str(line[3])[:-1])
		file.flush()
		return line[3]

#open file
if not os.path.exists(filename):
	file = open(filename, 'w')
	file.write("Datetime, watt\n")
else:
	file = open(filename,"a")
	file.write("\n")

print("Press ctrl+z to stop measuring, measurements will be saved to: {}" .format(filename))
while True:

	ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
	file.write(ts[:-3])

	getSNMP("192.168.178.45","1.3.6.1.4.1.28507.43.1.5.1.2.1.4.1")
	file.write("\n")