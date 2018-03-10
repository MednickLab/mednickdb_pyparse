from crontab import CronTab
import getpass
my_cron = CronTab(user=getpass.getuser())
for job in my_cron:
    if job.comment == 'AutoParse':
        my_cron.remove(job)
        my_cron.write()
