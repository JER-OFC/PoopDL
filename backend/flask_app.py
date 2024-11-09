#--> Standard module & library
import json

#--> Flask
from flask import Flask, Response, request
from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app=app)

#--> Local module
from python.poop import PoopFile, PoopLink

#--> Main
@app.route(rule='/')
def stream() -> Response:
    response: dict[str,str] = {
        'status'  : 'success',
        'service' : [
            {
                'method'   : 'POST',
                'endpoint' : 'generate_file',
                'url'      : '{}generate_file'.format(request.url_root),
                'params'   : ['url'],
                'response' : ['status', 'message', 'file']},
            {
                'method'   : 'POST',
                'endpoint' : 'generate_link',
                'url'      : '{}generate_link'.format(request.url_root),
                'params'   : ['domain', 'id'],
                'response' : ['status', 'message', 'link']}],
        'message' : 'hayo mau ngapain?'}
    return Response(response=json.dumps(obj=response, sort_keys=False), mimetype='application/json')

#--> Get file
@app.route(rule='/generate_file', methods=['POST'])
def getFile() -> Response:

    #--> Set default response
    result : dict[str,str] = {'status':'failed', 'message':'invalid params', 'file':[]}

    try:
        
        #--> Get params
        data : dict = request.get_json()
        url  : str  = data.get('url')

        if url:

            #--> Get file
            PF = PoopFile()
            PF.getAllFile(url)
            list_file : list = PF.file

            #--> Response condition
            if(len(list_file) != 0): result = {'status':'success', 'message':'', 'file':list_file}
            else: result = {'status':'failed', 'message':'file not found', 'file':[]}

    except Exception as e: result = {'status':'failed', 'message':'i dont know why error in poop app : {}'.format(str(e)), 'file':[]}
    return Response(response=json.dumps(obj=result, sort_keys=False), mimetype='application/json')

#--> Get link
@app.route(rule='/generate_link', methods=['POST'])
def getLink() -> Response:

    #--> Set default response
    result : dict[str,str] = {'status':'failed', 'message':'invalid params', 'link':''}

    try:

        #--> Get params
        data   : dict = request.get_json()
        domain : str = data.get('domain')
        id     : str = data.get('id')

        if domain and id:

            #--> Get link
            PL = PoopLink()
            PL.getLink(domain, id)
            link : str = PL.link

            #--> Response condition
            if link != '': result = {'status':'success', 'message':'', 'link':link}
            else: result = {'status':'failed', 'message':'link not found', 'link':''}

    except Exception as e: result = {'status':'failed', 'message':'i dont know why error in poop app : {}'.format(str(e)), 'file':[]}
    return Response(response=json.dumps(obj=result, sort_keys=False), mimetype='application/json')

#--> Initialization
if __name__ == '__main__':
    app.run(debug=True)

# list_url : list[str] = ['https://dood.cm/f/i37879otxpi', 'https://poop.vin/d/LPxbX8Mn4KZ', 'https://poop.pm/f/t8e12zcx7ra', 'https://poop.pm/f/p6mqkgysdr0', 'https://poop.pm/f/be20crhis8g', 'https://poop.pm/f/WTdgWsSnlnv']
# list_id  : list[str] = ['LPxbX8Mn4KZ', 'ggvl28sr6tuu', 'sjg5d1abyi5e', '6yz2q62slsir', 'JJOXFuOZoJL']