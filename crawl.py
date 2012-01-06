import datetime
from xml.etree.ElementTree import ElementTree
import urllib


# Get list of updated/new trials from clinicaltrials.gov
date = datetime.date.today().isoformat()
file_updates = 'rss_links/' + date + '.xml'
try:
    open = urllib.URLopener()
    open.retrieve('http://clinicaltrials.gov/ct2/results/rss.xml?recr=Open&lup_d=30&count=200', file_updates)
except IOError:
    print 'oops, something went wrong: Can\'t Open URL'

updates = []

#find links
tree = ElementTree()
tree.parse(file_updates)
links = tree.findall("channel/item/link")

#edit links to get xml formated files
for i in range(len(links)):
    link = (links[i].text)
    xml_link =link[:-40] + '?displayxml=true'
    updates.append(xml_link)

#retrieve trials from list of updates
for i in range(len(updates)):
    file = updates[i]
    open.retrieve(file, 'updates/' + file[-27:-16] + '.xml')
