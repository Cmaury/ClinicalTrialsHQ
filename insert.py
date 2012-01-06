from django.core.management import setup_environ
import settings
setup_environ(settings)
from trials.models import *
import os
from xml.etree.ElementTree import ElementTree

tree = ElementTree()
#Get files from update directory and read them to table


for filename in os.walk("./updates"):
   try:
       Store(filename) 
   except :    
       break

   os.remove(i)    

class Store(filename):

    def __init__(self, filename):
        self.filename = filename
        
    element_text_pairs = {}
    xml = tree.parse(filename)
    #parses xml into dictionary
    def unzip1(xml):
        for element in list(xml):
            element_text_pairs[element.tag] =  element.text
            unzip1(element)
    
    #iterates over dictionary, inserting data into fixture
    def insert1(k,v):
        conditions = {}
        keywords = {}
        mesh_terms ={}
        location = {}
        contact = {}
        criteria = {}
        conditions['pk'] = int(Conditions.objects.order_by('-id')[0].id)
        keywords['pk'] = int(Keyword.objects.order_by('-id')[0].id)
        mesh_terms['pk'] = int(Mesh_key.objects.order_by('-id')[0].id)
        location['pk'] = int(Locations.objects.order_by('-id')[0].id)
        criteria['pk'] = int(Critera.objects.order_by('-id')[0].id)
        contact['pk'] = Contact.objects.order_by('-trial_id')[0].trial_id

        #trials logic
        if k == 'nct_id':
            trial_id = v
        if k == 'brief_title':
            child_test = list(k)
            if child_test[0].tag != 'textblock':
                brief_title = v
            else:    
                brief_title = xml.find(k +'/textblock')
                brief_title = brief_title[0].text
        if k == 'official_title':
            official_title = v
        if k == 'brief_summary':
            child_test = list(k)
            if child_test[0].tag != 'textblock':
                brief_summary = v
            else:    
                brief_summary= xml.find(k +'/textblock')
                brief_summary = brief_title[0].text
        if k =='detailed_description':
            child_test = list(k)
            if child_test[0].tag != 'textblock':
                detailed_description = v
            else:    
                brief_description = xml.find(k +'/textblock')
                brief_description = brief_title[0].text
        if k == 'overall_status':
            overall_status = v
        if k == 'phase':
            phase = v
        if k == 'enrollment':
            enrollment = v
        if k == 'study_type':
            study_type = v
        if k == 'condition':
            child_many = tree.findall('condition')
            for i in child_many:
                fixtures = fixtures + '"pk":' + conditions['pk']+ 1 +',\n\
                "model": trials.conditions,\n\
                "fields": {\n\
                    "trial_id": ' + trial_id +',\n\
                    "keyword": '+ [i].text +',\n\
                }'
                conditions['list'].append(conditions['pk']+1)
                conditions['pk'] +=1

        if k == 'elligibility':
            elligibility = v
        if k == 'criteria':
            child_test = list(k)
            if child_test[0].tag != 'textblock':
                fixture = fixture + '"pk": ' + criteria['pk'] + 1  + ',\n\
                "model": ' + trials.criteria + ',\n\
                "fields": {\n\
                    "trial_id":  ' + trial_id + ',\n\
                    "gender": ' + gender + ',\n\
                    "minimum_age": ' + minimum_age + ',\n\
                    "maximum_age": ' + maximum_age + ',\n\
                    "healthy_participants": ' + healthy_participants + ',\n\
                    "textblock": '',\n\
                }'
            else:
                  fixture = fixture + '"pk": ' + criteria['pk'] + 1 + ',\n\
                  "model": ' + trials.criteria + ',\n\
                  "fields": {\n\
                      "trial_id":  "",\n\
                      "gender": "",\n\
                      "minimum_age": "",\n\
                      "maximum_age": "",\n\
                      "healthy_participants": "",\n\
                      "textblock": ' + child_test[0].text + ',\n\
                  }'

        if k == 'overall_contact' or  k == 'contact':
            fixture = fixture + '"pk": ' + contact['pk'] + 1 + ',\n\
            "model": ' + trials.contact + ',\n\
            "fields": {\n\
                    "trial_id": ' + trial_id + ',\n\
                    "last_name": ' + last_name + ',\n\
                    "phone": ' + phone + ',\n\
                    "email": ' + email + ',\n\
            }'
            
        if k == 'location':
            child_many = tree.findall('location')
            for i in child_many:
                child = list(i)
                address = list(child[1])
                fixture = fixture + '"pk": '+ locations['pk'] + ',\n\
                "model": trials.locations,\n\
                "fields": {\n\
                    "trial_id": ' + trial_id + ',\n\
                    "facility": ' + child[0].text  + ',\n\
                    "city": ' + address[0].text + ',\n\
                    "state": ' + address[1].text+ ',\n\
                    "zip": ' +address[2].text+ ',\n\
                    "country": ' + address[3].text + ',\n\
                }'
                locations['list'].append(locations['pk']+1)
                locations['pk'] +=1                

        if k == 'lastchanged_date':
            lastchanged_date = v
        if k == 'firstreceived_date':
            firstreceived_date = v
        if k == 'keyword':
            child_many = tree.findall('keyword')
            for i in child_many:
                fixtures = fixtures + '"pk":' + keywords['pk']+ 1 +',\n\
                "model": trials.keyword,\n\
                "fields": {\n\
                    "trial_id": ' + trial_id +',\n\
                    "keyword": '+ [i].text +',\n\
                }'
                keywords['list'].append(keywords['pk']+1)
                keywords['pk'] +=1

        if k == 'mesh_term':
            child_many = tree.findall('mesh_term')
            for i in child_many:
                fixtures = fixtures + '"pk":' + mesh_terms['pk']+ 1 +',\n\
                "model": trials.mesh_term,\n\
                "fields": {\n\
                    "trial_id": ' + trial_id +',\n\
                    "keyword": '+ [i].text +',\n\
                }'
                mesh_terms['list'].append(mesh_terms['pk']+1)
                mesh_terms['pk'] +=1
        #criteria logic
        if k == 'gender':
            gender = v
        if k == 'minimum_age':
            minimum_age
        if k == 'maximum_age':
            maximum_age = v
        if k == 'healthy_volunteers':
            healthy_colunteers = v
        
        #contact logic
        if k == 'phone':
            phone = v
        if k == 'email':
            email = v
        if k == 'last_name':
            last_name = v
        
        fixture = '{\n\
        "pk": '+ trial_id + ',\n\
        "model": trials.trial,\n\
        "fields": {\n\
                "trial_id": ' + trial_id + ',\n\
                "brief_title": ' + brief_title + ',\n\
                "official_title": ' + official_title + ',\n\
                "brief_summary": ' + brief_summary + ',\n\
                "detailed_Description": ' + detailed_description + ',\n\
                "overall_status": ' + overall_status + ',\n\
                "phase": ' + phase + ',\n\
                "enrollment": ' + enrollment + ',\n\
                "study_type": ' + study_type + ',\n\
                "condition": ' +  conditions['list'] + ',\n\
                "elligibility": ' + elligibility + ',\n\
                "criteria":  ' + criteria['pk'] + 1 + ',\n\
                "overall_contact": ' + contact['pk'] + 1 + ',\n\
                "location":  ' + location['list'] + ',\n\
                "lastchanged_date": ' + lastchanged_date + ',\n\
                "firstreceived_date": ' + firstreceived_date + ',\n\
                "keyword": ' + keywords['list'] + ',\n\
                "condition_mesh": ' + mesh_terms['list'] + ',\n\
        }\n\
        \n\
        "pk": ' + contact['pk'] + ',\n\
        "model": ' + trials.contact + ',\n\
        "fields": {\n\
                "trial_id": ' + trial_id + ',\n\
                "last_name": ' + last_name + ',\n\
                "phone": ' + phone + ',\n\
                "email": ' + email + ',\n\
        }'

        fixture = fixture + '}'
        return fixture   


Store.unzip1(xml)
for k,v in element_text_pairs.iteritems():
    Store.insert1(k,v)
#f.open(filename - 'xml' + 'json')    
#os.write(fixture) 
#f.close
#os.system('manage.py loaddata ' +filename - 'xml' + 'json') 
