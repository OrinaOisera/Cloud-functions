import json
import random
from google.cloud import storage
import xmltodict 

storage_client = storage.Client()
TICKETS_BUCKET = 'kizee'

def raise_ticket(request):
    content_type = request.headers['content-type'] 
    
    if content_type == 'application/json':
        name = request.json.get('name')
        issue = request.json.get('issue')
    elif content_type == 'application/octet-stream':
        temp_data = request.data.decode("utf-8")
        words = temp_data.split()
        name = words[words.index('name:') + 1]
        issue = temp_data.split("issue", 1) [1]
    elif content_type == 'text/plain' :
        temp_data = request.data.decode('utf-8')
        words =temp_data.split()
        name = words[words.index('name:') + 1]
        issue = temp_data.split("issue:", 1)[1]
    elif content_type == 'application/x-www-form-urlencoded':
        name = requests.form.get('name')
        issue = requests.form.get('issue')
    elif content_type == 'text/xml':
        temp_data = xmltodict.parse(request.data)
        name = temp_data['ticketraiser']['@name']
        issue = temp_data['ticketraiser']['issue']
        
        
    else:
        raise ValueError ("unknown content type {}" . format(content_type))
        
        
    id = random.randint(1000,2000)
    
    tickets_dict={}
    tickets_dict['id']=id
    tickets_dict['name']=name
    tickets_dict['issue']=issue
    
    bucket = storage_client.get_bucket(TICKETS_BUCKET)
    blob = bucket.blob('parsed_tickets_data/tickets.json')
    if blob.exists():
        blob.download_to_filename('/tmp/tickets.json')
    with open("/tmp/tickets.json", "a") as fp:
        json.dump(tickets_dict,fp,indent=2)
        
    blob.upload_from_filename('/tmp/tickets.json')
    return 'Tickets generated with id, {}'.format(id)
        
