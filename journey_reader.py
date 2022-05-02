# Turn Journey Cloud JSON files into Evernote ENEX files

import os
import re
import json
from datetime import datetime
import sys

jsonfiles = []
for root, dirs, files in os.walk('journey'):
    for file in files:
        if file.endswith('.json'):
            jsonpath = os.path.join(root, file)

            reader = open(jsonpath, 'r+')
            data = json.loads(reader.read())
            reader.close()

            created = datetime.fromtimestamp(data['date_journal']/1000)
            modified = datetime.fromtimestamp(data['date_modified']/1000)
            created_enex = created.strftime(f"%Y%m%dT%H%M%SZ")
            modified_enex = modified.strftime(f"%Y%m%dT%H%M%SZ")
            title = created.strftime(f"%Y-%m-%d %H:%M")
            id = data['id']
            journeytags = data['tags']
            tags=''
            if len(journeytags)>0:
                for tag in journeytags:
                    tags += f'<tag>{tag}</tag>'
                        
            text = f"""
                Imported from Journey<br/>
                Created: {created}<br/>
                Modified: {modified}<br/>
                Journey ID: {id}<br/>
                Journey tags: {tags}<br/><br/><br/>
                Entry:<br/><br/>{re.sub(r'<.*?>', '', data['text'])}"""
            
            enexcontents = f"""
                <note>
                    <title>{title}</title>
                    <content>
                        <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                        <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
                        <en-note><div>{text}</div></en-note>
                        ]]>
                    </content>
                    <created>{created.strftime("%Y%m%dT%H%M%SZ")}</created>
                    <updated>{modified.strftime("%Y%m%dT%H%M%SZ")}</updated>
                    {tags}
                    <note-attributes></note-attributes>
                    %(resources)s
                </note>"""

            enexpath = jsonpath.replace('.json','.enex').replace('journey','evernote')
            writer = open(enexpath, 'w')#'x')
            writer.write(enexcontents)
