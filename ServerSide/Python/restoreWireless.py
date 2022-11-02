import os
import time
os.system('cp /etc/config/wireless.ori /etc/config/wireless')
os.system('/sbin/wifi reload wlan1')
time.sleep(1.5)
os.system('/sbin/wifi reload')
