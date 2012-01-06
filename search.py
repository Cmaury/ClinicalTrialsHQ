from haystack.indexes import *
from haystack import site
from trials_site.trials.models import *

class ConditionIndex(SearchIndex):
    trial_id = indexes.CharField(model_attr='trial_id')
    keyword = indexes.CharField(document=True, use_Template=True)

    def get_model(self):
        return Condition

class KeywordIndex(SearchIndex):    
    trial_id = indexes.CharField(model_attr='trial_id')
    keyword = indexes.CharField(document=True, use_Template=True)

    def get_model(self):
        return Keyword    

