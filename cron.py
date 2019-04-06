#!/usr/bin/env python3
import os
from crontab import CronTab

cwd = os.getcwd()

# Initialise cron
cron = CronTab(user='pi')
cron.remove_all()

# Monitor and Notify
monitor_job_script = "%s/monitorAndNotify.py" % cwd
monitor_job = cron.new(command=monitor_job_script)
monitor_job.minute.every(1)

# Bluetooth
bluetooth_job_script = "%s/greenhouseBluetooth.py" % cwd
bluetooth_job = cron.new(command='/')
bluetooth_job.minute.every(1)

cron.write()