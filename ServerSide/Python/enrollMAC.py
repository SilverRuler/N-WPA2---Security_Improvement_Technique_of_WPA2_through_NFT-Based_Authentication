import sys
import os

STAmac = sys.argv[1]
STAmac = STAmac.upper()
temp = open("/etc/config/wireless", 'r')
tempbr = temp.read()
temp.close()

bu = open("/etc/config/wireless", 'w')
bu.writelines(tempbr)

bu.write("        list maclist '")
bu.write(STAmac)
bu.write("'")
bu.write("\n")
bu.close()

bu = open("./ssidName.txt", 'w')
ssidName = sys.argv[2]
bu.write(ssidName)
bu.close()

os.system('/sbin/wifi reload wlan1')
