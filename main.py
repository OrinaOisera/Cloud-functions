import json
import random

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
        
    else:
        raise ValueError ("unknown content type {}" . format(content_type))
        
        
    id = random.randint(1000,2000)
    return'Ticket generated with id, {}'.format(id)