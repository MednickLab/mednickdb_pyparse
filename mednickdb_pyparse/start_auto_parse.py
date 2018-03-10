from crontab import CronTab
import getpass

# init cron
cron = CronTab(user=getpass.getuser())

# add new cron job
job = cron.new(command='python mednickdb_auto_parse.py', comment='AutoParse')

# job settings
job.minute.every(1)

cron.write()