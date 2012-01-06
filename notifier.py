import re
from django.core.mail import EmailMessage
from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.template.loader import render_to_string
from trials.models import *
from datetime import datetime, date


today = date.today()
conditions= []
notifications= {}
email_list = []

Updates = Trial.objects.filter(lastchanged_date = today)
#Grab conditions from trials updated today
for i in Updates.all():
    for j in i.condition.all():
        append = True
        for k in conditions:
            if k == j.keyword:
                append = False
        if append is True:
            conditions.append(j.keyword)

#check if notifications exist for that condition
for i in conditions:
    new_conds = Notification.objects.filter(condition__icontains=i)
    for j in new_conds:
        for k in j.email.all():
            email_list.append(k.email)
        notifications[j.condition] = email_list
        
#send notification email
for k,v in notifications.iteritems():
    condition = str(k)
    spaced = ''
    for i in range(len(condition)):
        if re.match('\s',condition[i]):
            spaced = spaced + '+'
        else:
            spaced = spaced + condition[i]
    for i in v:
        message = render_to_string('notify.html', {'condition_url': spaced,'condition':k,'email': i})
        email = EmailMessage('There is a new trial for ' + k, message , 'no-reply@clinicaltrialsHQ.com','',v,'')
        try:
            email.send(fail_silently=False)
        except:
            log = open('/root/medical_trials/trials_site/email_log.txt', "a")
            log.write("email failed to send" + k +" : "+ i )
