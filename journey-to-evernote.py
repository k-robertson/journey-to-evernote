# Turn Journey Cloud JSON files into Evernote ENEX files

import os
import re
import json
from datetime import datetime

# find JSON files in folder 'journey' (relative path)
for root, dirs, files in os.walk('journey'):
    for file in files:
        if file.endswith('.json'):

            # get contents of Journey JSON file
            jsonpath = os.path.join(root, file)
            reader = open(jsonpath, 'r+')
            data = json.loads(reader.read())
            reader.close()

            # get details about the Journey entry
            created = datetime.fromtimestamp(data['date_journal']/1000)
            modified = datetime.fromtimestamp(data['date_modified']/1000)
            id = data['id']
            journeytags = data['tags']
            tags=''
            if len(journeytags)>0:
                for tag in journeytags:
                    tags += f'<tag>{tag}</tag>'
            entry = data['text'] 

            # set up journal entry to include Journey ID & tags
            # entry = re.sub(r'<.*?>', '', data['text'])
            entry = entry.replace('\n','<br/>')
            contents = f'Journey ID: {id}<br/>Journey tags: {tags}<br/><br/><br/>{entry}'
            
            # insert entry into Evernote's ENEX file format and save to ENEX file
            title = 'Journey: ' + created.strftime(f"%Y-%m-%d %H:%M")
            enexcontents = f'<note><title>{title}</title><content><![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note><div>{contents}</div></en-note>]]></content><created>{created.strftime("%Y%m%dT%H%M%SZ")}</created><updated>{modified.strftime("%Y%m%dT%H%M%SZ")}</updated>{tags}</note>'

            # create ENEX file and insert contents
            enexpath = jsonpath.replace('.json','.enex').replace('journey','evernote')
            writer = open(enexpath, 'w')#'x')
            writer.write(enexcontents)
