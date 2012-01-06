from store import Store
import os
import logging
import traceback

log = logging.getLogger('parse_logs')
log.setLevel(logging.WARN)
#log.captureWarnings(True)
fh=logging.FileHandler('/root/medical_trials/trials_site/logs/parse.log')
fh.setLevel(logging.ERROR)
log.addHandler(fh)

#run store on files in a given directory
for root, dir, files in os.walk("./updates"):
    for i in files:
        record = root +'/' + i
        print record        
        try:
            Store(record)
        except Exception, e:
            log.error('Import failed ' + repr(e))
        os.rename(record, './imported_files/' + i)
