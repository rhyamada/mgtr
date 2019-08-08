from flask import Flask, jsonify
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        api = Finding(appid=os.environ['EBAY'], config_file=None)
        api_request = {
            'itemFilter': [
                {'name': 'ListingType','value': 'Auction'},
                {'name': 'Seller','value': os.environ['SELLERS'].split(' ')},
                {'name': 'MaxPrice', 'value': '10', 'paramName': 'Currency', 'paramValue': 'USD'},
            ],
            'sortOrder': 'EndTimeSoonest',
            'paginationInput': {
                'entriesPerPage': '10',
                'pageNumber': '1' 	 
            },        
        }    
        response = api.execute('findItemsAdvanced', api_request)
        return jsonify(response.dict())
    except ConnectionError as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ['PORT'])