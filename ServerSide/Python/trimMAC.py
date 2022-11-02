with open('/etc/config/wireless', 'r') as fin:
    data = fin.read().splitlines(True)
with open('/etc/config/wireless', 'w') as fout:
    fout.writelines(data[:-1])
