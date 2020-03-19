# scheduler.py

from newsproject import execute
import pandas as pd

client_summary = pd.read_csv('client_summary.txt', sep='\t')

# execute every three hours
frequency = 3        
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
sched.add_job(execute, 'interval',
             hours=frequency,args=[client_summary])

# Start the scheduler
# sched.start()
# sched.pause()
# sched.resume()