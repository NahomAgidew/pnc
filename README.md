#Portable Network Client

#Overview
pnc is a portable computer networking utility for reading from and writing to network connections using TCP.
It runs on a any platform (Windows, Mac, Linux, Raspberry pi) or any system which run Python without the
need for any dependencies.

#Usage
Establish a TCP connection with a target host: python pnc.py -t [target_host] -p [port]
Listen to incoming connections on specified port: python pnc.py -l -p [port]
Transfer file to server: python pnc.py -t [target_host]  -p [port] -u c:\\target.txt -d /temp/target.txt

#Copyright
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
