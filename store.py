from datetime import datetime
from datetime import date
from django.core.management import setup_environ
import settings
setup_environ(settings)
from trials.models import *
from xml.etree.ElementTree import ElementTree
import json
import logging
import os
import settings
import traceback
tree = ElementTree()
log = logging.getLogger('parse_logs')
log.setLevel(logging.WARN)
#log.captureWarnings(True)
fh=logging.FileHandler('/root/medical_trials/trials_site/logs/parse.log')
fh.setLevel(logging.ERROR)
log.addHandler(fh)
def Store(filename):
    trial_id = ''
    brief_title = ''
    official_title = ''
    brief_summary = ''
    detailed_description = ''
    overall_status = ''
    phase = ''
    enrollment = ''
    study_type = ''
    eligibility = ''
    criteria = ''
    overall_contact = ''
    location = ''
    lastchanged_date = ''
    firstreceived_date = ''
    keyword = ''
    mesh_term = ''
    gender = ''
    minimum_age = ''
    maximum_age = ''
    healthy_volunteers = ''
    phone = ''
    email = ''
    last_name = ''
    fixtures = []
    missing_data = []
    conditions = {}
    keywords = {}
    mesh_terms ={}
    locations = {}
    contact = {}
    criteria = {}
    conditions['pk'] = int(Conditions.objects.order_by('-id')[0].id)
    keywords['pk'] = int(Keyword.objects.order_by('-id')[0].id)
    mesh_terms['pk'] = int(Mesh_key.objects.order_by('-id')[0].id)
    locations['pk'] = int(Locations.objects.order_by('-id')[0].id)
    criteria['pk'] = int(Criteria.objects.order_by('-id')[0].id)
    contact['pk'] = int(Contact.objects.order_by('-id')[0].id)
    contact['list'] = []
    criteria['list'] = []
    conditions['list'] = []
    keywords['list'] = []
    mesh_terms['list'] = []
    locations['list'] = []
    xml = tree.parse(filename)
    trial_id = xml.find('id_info/nct_id').text
#Parse Brief Title
    try:
        if xml.find('brief_title')[0].tag == 'textblock':
            brief_title = unicode(xml.find('brief_title/textblock').text, 'utf-8')
        else:
            brief_title = unicode(xml.find('brief_title/').text, 'utf-8')
    except:
        missing_data.append('brief_title')
#Parse Official Title
    try:
        if xml.find('official_title')[0].tag == 'textblock':
            official_title = unicode(xml.find('official_title/textblock').text, 'utf-8')
        else:
            official_title = unicode(xml.find('official_title').text, 'utf-8')
    except:
        missing_data.append('official_title')
#Parse Brief Summary
    try:
        if xml.find('brief_summary')[0].tag == 'textblock':
            brief_summary = unicode(xml.find('brief_summary/textblock').text, 'utf-8')
        else:
            brief_summary = unicode(xml.find('brief_summary').text, 'utf-8')
    except:
        missing_data.append('brief_summary')
#Parse Detailed Description
    try:
        if xml.find('detailed_description')[0].tag == 'textblock':
            detailed_description = unicode(xml.find('detailed_description/textblock'), 'utf-8')
        else:
            detailed_description = unicode(xml.find('detailed_description'), 'utf-8')       
    except:
        missing_data.append('detailed_description')
    try:
        overall_status = unicode(xml.find('overall_status').text, 'utf-8')
    except:
        missing_data.append('overall_status')
    try:
        phase = unicode(xml.find('phase').text, 'utf-8')
    except: 
        missing_data.append('phase')
    try:
        enrollment = unicode(xml.find('enrollment').text, 'utf-8')
    except:
        missing_data.append('enrollment')
    try:
        study_type = unicode(xml.find('study_type').text, 'utf-8')  
    except:
        missing_data.append('study_type')
    try:
        lastchanged_date = xml.find('lastchanged_date').text
        lastchanged_date = datetime.strptime(lastchanged_date, '%B %d, %Y')
        lastchanged_date = date.isoformat(lastchanged_date)
    except:
        missing_data.append('lastchanged_date')
    try:
        firstreceived_date = xml.find('firstreceived_date').text
        firstreceived_date = datetime.strptime(firstreceived_date, '%B %d, %Y')
        firstreceived_date = date.isoformat(firstreceived_date)
    except:
        missing_data.append('firstreceived_date')
    try:
        gender = unicode(xml.find('eligibility/gender').text, 'utf-8')
    except:
        missing_data.append('gender')
    try:
        minimum_age = xml.find('eligibility/minimum_age').text
    except:
        missing_data.append('minimum_age')
    try:
        maximum_age = xml.find('eligibility/maximum_age').text
    except:
        missing_data.append('maximum_age')
    try:
        healthy_volunteers = unicode(xml.find('eligibility/healthy_volunteers').text, 'utf-8')
    except:
        missing_data.append('healthy_volunteers')
    try:
        if xml.find('overall_official').tag == 'overall_official':
            tag = xml.find('overall_official').tag
        else:
            tag = xml.find('overall_contact').tag
    except:
        missing_data.append('overall_contact')
    try:
        last_name = unicode(xml.find(tag + '/last_name').text, 'utf-8')
    except:
        missing_data.append('last_name')    
    try:
        phone = xml.find(tag + '/phone').text       
    except:
        missing_data.append('phone')    
    try:
        email = xml.find(tag +'/email').text
    except:
        missing_data.append('email')
##Multiple entries
#condition
    child_many = xml.findall('condition')
    for i in child_many:
        cond = {}
        cond_fields = {}
        cond_fields['trial_id'] = trial_id
        cond_fields['keyword'] = unicode(i.text, 'utf-8')
        if len(cond_fields['keyword']) >= 100:
            cond_fields['keyword'] = cond_fields['keyword'][:200]
        cond['pk'] = conditions['pk']+ 1
        cond['model'] = 'trials.conditions'
        cond['fields'] = cond_fields    
        conditions['list'].append(conditions['pk']+1)
        conditions['pk'] +=1
        fixtures.append(cond)
#criteria
    child_test = xml.findall('eligibility/criteria')
    if child_test[0].tag != 'textblock':
        crit = {}
        crit_fields = {}
        crit_fields['trial_id'] = trial_id
        crit_fields['gender'] = gender
        crit_fields['minimum_age'] = minimum_age
        crit_fields['maximum_age'] = maximum_age
        crit_fields['healthy_volunteers'] = healthy_volunteers
        crit_fields['textblock'] = ''
        crit['pk'] = criteria['pk'] + 1
        crit['model'] = 'trials.criteria'
        crit['fields'] = crit_fields
        criteria['list'].append(crit['pk'])
        fixtures.append(crit)
    else:
        crit = {}
        crit_fields = {}
        crit_fields['trial_id'] = ''
        crit_fields['gender'] = ''
        crit_fields['minimum_age'] = ''
        crit_fields['maximum_age'] = ''
        crit_fields['healthy_volunteers'] = ''
        crit_fields['textblock'] = unicode(child_test[0].text, 'utf-8')
        crit['pk'] = criteria['pk'] + 1
        crit['model'] = 'trials.criteria'
        crit['fields'] = crit_fields
        criteria['list'].append(crit['pk'])
        fixtures.append(crit)
    for k,v in crit_fields.iteritems():
        if k[-3:] == 'age' and type(v) is str:
            try:
                crit_fields[k] = int(v[:2])
            except:
                crit_fields[k] = 99
#keywords
    child_many = xml.findall('keyword')
    for i in child_many:
        key = {}
        key_fields = {}
        key_fields['trial_id'] = trial_id
        key_fields['keyword'] = unicode(i.text, 'utf-8')
        if len(key_fields['keyword']) >= 200:
               key_fields['keyword'] = key_fields['keyword'][:200]
        key['pk'] = keywords['pk']+ 1
        key['model'] = 'trials.keyword'
        key['fields'] = key_fields
        fixtures.append(key)
        keywords['list'].append(keywords['pk']+1)
        keywords['pk'] +=1      
#Mesh_terms
    child_many = xml.findall('mesh_term')
    for i in child_many:
        mesh = {}
        mesh_fields = {}
        mesh_fields['trial_id'] = trial_id
        mesh_fields['keyword'] = unicode(i.text, 'utf-8')
        if len(mesh_fields['keyword']) >= 200:
            mesh_fields['keyword'] = mesh_fields['keyword'][:200]  
        mesh['pk'] = mesh_terms['pk']+ 1
        mesh['model'] = 'trials.mesh_key'
        mesh['fields'] = mesh_fields
        fixtures.append(mesh)
        mesh_terms['list'].append(mesh_terms['pk']+1)
        mesh_terms['pk'] +=1
#Locations
    child_many = xml.findall('location')
    for i in child_many:
        child = list(i)
        for i in range(len(list(child[0]))):
            if  list(child[0])[i].tag == 'address':
                address = list(child[0])[i]
        loc = {}
        loc_fields = {}                 
        loc_fields['trial_id'] = trial_id
        loc_fields['facility'] = list(child[0])[0].text
        if type(loc_fields['facility']) is not unicode:
            unicode(loc_fields['facility'], 'utf-8')
        if len(loc_fields['facility']) >= 200:
            loc_fields['facility']= loc_fields['facility'][:200]
        for i in range(len(address)):
            if address[i].tag == 'city':
                loc_fields['city'] = unicode(address[i].text, 'utf-8')
            if address[i].tag == 'state':
                loc_fields['state'] = unicode(address[i].text, 'utf-8')
            if address[i].tag == 'zip':
                loc_fields['zip'] = unicode(address[i].text, 'utf-8')
            if address[i].tag == 'country':
                loc_fields['country'] = unicode(address[i].text, 'utf-8')
        loc['pk'] = locations['pk']+ 1
        loc['model'] = 'trials.locations'
        loc['fields'] = loc_fields
        fixtures.append(loc)
        locations['list'].append(locations['pk']+1)
        locations['pk'] +=1
#contacts
    cont = {}
    cont_fields = {}
    cont_fields['trial_id'] = trial_id
    cont_fields['last_name'] = last_name
    cont_fields['phone'] = phone
    cont_fields['email'] = email
    cont['pk'] = contact['pk']
    cont['model'] = 'trials.contact'
    cont['fields'] = cont_fields
    contact['list'].append(contact['pk'])
    fixtures.append(cont)
#Fixtures
    trial = {}
    trial_fields = {}
    trial_fields['trial_id'] = trial_id
    trial_fields['brief_title'] = brief_title
    trial_fields['official_title'] = official_title
    trial_fields['brief_summary'] = brief_summary
    trial_fields['detailed_Description'] = detailed_description
    trial_fields['overall_Status'] = overall_status
    trial_fields['phase'] = phase
    trial_fields['enrollment'] = enrollment
    trial_fields['study_type'] = study_type
    trial_fields['condition'] = conditions['list']
    trial_fields['criteria'] = criteria['list']
    trial_fields['overall_contact'] = contact['pk']
    trial_fields['location'] = locations['list']
    trial_fields['lastchanged_date'] = lastchanged_date
    trial_fields['firstreceived_date'] = firstreceived_date
    trial_fields['keyword'] = keywords['list']
    trial_fields['condition_mesh'] = mesh_terms['list']
    trial['pk'] = trial_id
    trial['model'] = 'trials.trial'
    trial['fields'] = trial_fields
    fixtures.append(trial)
#Check for empty fields and replace them with NULL
    for i in fixtures:
        for k,v in i.items():
            if v == '':
                i[k] = 'NULL'
            elif type(v) is dict:
                 for j,z in v.items():
                      if z == '':
                          v[j] = 'NULL'
                      elif type(z) is list and len(z)==0:
                          del v[j] 
            elif type(v) is list:
                if len(v) == 0:
                    del i[k]
#check for missing fields and log
    if len(missing_data) > 0:
        for i in missing_data:
            log.error('missing data ' + i +' from ' + trial_id)
#output
    format =json.dumps(fixtures)
    print format
    path =str('./fixtures/' + filename[10:-3] + 'json')
    try:
      output =  open(path, "w")
    except:
        log.error("failed to open " + path)    
        return 'error, see parse.log'    
    output.write(format) 
    output.close()
    try:
        os.system('python manage.py loaddata ' + path)
    except Warning:
        log.error("failed to import fixture from file " + path)
        log.warning("failed to import fixture from file " + path)
        return 'error, see parse.log'
