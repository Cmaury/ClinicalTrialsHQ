from django.contrib.sitemaps import Sitemap
from trials_site.trials.models import *

class TrialSitemap(Sitemap):
    def items(self):
        return Trial.objects.all()
        
    


