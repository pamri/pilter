"""
File for specifying the filters handled by mailhandler.


"""
# Required import
import helpers as h

# Imports,etc., for sample configuration
import sys
sys.path.append('/path/to/django/project')
from django.core.management import setup_environ
from django_project import settings
setup_environ(settings)
from django_app import models

def run_filter(instance):
"""
run_filter function should be retained and all your filters should go under this function. 
"""
   # Sample filters

    # We filter mail based on the sender and 'failure' text in the body
    # grep for lines matchine certain keywords , split the line using ':' delimiter 
    # added it to a list and update a mysql database using the Django libraries
    t = []  
    if (h.contains(instance.sender, 'alerter@xyz.net') and 
    h.contains(instance.body, 'failure')):
        for each_line in h.line_match(instance.body,
        ['URL', 'Project'):
            t.append(each_line.split(': ')[1])
        print "Alert for %(url)s belonging to %(project)s\n" % \
        {"url":t[0], "project":t[1]} 
        models.monitors(url=t[0], project=t[1]).save()
            
    # Real example - We filter mails coming from Keynote, the site monitoring service.
    # We find the project, select the status for the project based on the subject and then print the same
    if (h.contains(instance.sender, 'alert@keynote.com')):
        project = instance.body[instance.body.find('EST')+4:].split('\n')[0]
        if h.contains(instance.subject, 'Now OK'):
            status = "Now OK"
        elif h.contains(instance.subject, 'Crit'):
            status = "Critical"
        else:
            status = "Unknown"
        keynote_url = h.line_match(instance.body, 'my.keynote.com')
        performance = float(h.line_match(instance.body, 
        'secs').split(' ')[0])
        date = instance.date_d

        print "%(status)s for %(project)s : %(performance)f secs\n" % \
        {"status":status, "project":project, "performance":performance}

    # We print the entire body of the message sometimes based on the sender and subject
    if (h.contains(instance.sender, 'servicedesk@xyz.com') and
    h.contains(instance.subject, 'Notification')):
        print instance.body
