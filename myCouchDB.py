'''
couchDB
Updates couchDB document and adds attachments to existing documents.
 
@author: Adam James
'''

import couchdb
import io
import json
import requests

class myCouchDB():
    
    #What we'll need
    COUCH_SERVER = db = dbname = id = rev = filename = post_payload = image_url = ''
    
    def select_db(self):    
        missing_value = []
        # Make sure we have what we need first.    
        if self.COUCH_SERVER == '':
            missing_value.append('server')
        elif self.dbname == '':
            missing_value.append('database name')       
        amount = len(missing_value)
        # Moment of truth
        if ( amount == 0 ):
            couch   = couchdb.Server(self.COUCH_SERVER)
            self.db = couch[self.dbname]
            return self
        else:
            return False #OR return missing_value for debuggging            

    def insert_doc(self):
        # Make sure we have what we need first.    
         if self.post_payload != '':            
            doc      = self.post_payload
            obj      = self.db.save(doc)
            self.id  = obj[0]
            self.rev = obj[1]
            return self
         else:
             return False
        
    def put_doc_attachment(self):
        # Make sure we have what we need first.
        if self.filename != '':
            filename = self.filename
            doc      = {'_id':self.id, '_rev':self.rev}
            file     = open(filename, 'rb')
            self.db.put_attachment(doc, content=file)
            return self
        else:
            return False           

    def get_doc_by_id(self,id):
        doc = db[self.id]
        return doc
    
    def get_all(self):
        docs = []
        for id in self.db:
            docs.append(id)        
        return docs
    
    def delete_doc(self,id):
        doc = self.get_doc_by_id(id)
        return self.db.delete(doc)
           
    def get_doc_image_by_id(self):
        url = self.COUCH_SERVER + self.dbname + '/' + self.id
        r = requests.get(url)
        if (r.status_code == 200):
            theJSON = json.loads(r.text)
            for key in theJSON['_attachments'].keys(): 
                image = key    
            self.image_url = url + '/'+ image
            return self.image_url
        else:
            return False      