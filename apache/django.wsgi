import os
import sys
sys.path.append('/root/medical_trials/')
sys.path.append('/root/medical_trials/trials_site/')
# The first part of this module name should be identical to the directory name
# of the OSQA source.  For instance, if the full path to OSQA is
# /home/osqa/osqa-server, then the DJANGO_SETTINGS_MODULE should have a value
# of 'osqa-server.settings'.

os.environ['DJANGO_SETTINGS_MODULE'] = 'trials_site.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
