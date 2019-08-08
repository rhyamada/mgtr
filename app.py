from flask import Flask, jsonify, request
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import os,json,re
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
ire = re.compile('P(?P<days>[0-9]+)DT(?P<hours>[0-9]+)H(?P<minutes>[0-9]+)M(?P<seconds>[0-9]+)S')

@app.route('/')
def index():
    price = float(request.values.get('p',10))
    hours = float(request.values.get('h',8))
    try:
        d = datetime.now()+timedelta(seconds=3600*hours)
        api = Finding(appid=os.environ['EBAY'], config_file=None)
        api_request = {
            'itemFilter': [
                {'name': 'Currency', 'value':'USD'},
                {'name': 'ListingType','value': 'Auction'},
                {'name': 'Seller','value': os.environ['SELLERS'].split(' ')},
                {'name': 'MaxPrice', 'value': price, 'paramName': 'Currency', 'paramValue': 'USD'},
                {'name': 'EndTimeTo',   'value': d.isoformat()}
            ],
            'sortOrder': 'EndTimeSoonest',
        }
        res = api.execute('findItemsAdvanced', api_request).dict()
        html = '' 
        if 'item' in res['searchResult']:
            for i in res['searchResult']['item']:
                i['json']=json.dumps(i,indent=4)
                i['price']=float(i['sellingStatus']['currentPrice']['value'])+float(i['shippingInfo']['shippingServiceCost']['value'])
                if i['price']>price:
                    continue
                m = ire.match(i['sellingStatus']['timeLeft'])
                if m:
                    i['sellingStatus']['timeLeft'] = str(timedelta(**{k:int(v) for k,v in m.groupdict().items()}))
                html = html + '''
                
                <details>
                    <summary>
                    <code style="white-space:pre;"><span style="display:inline-block;width:16px;"><img style="height:1em;" src="{galleryURL}"/></span>[{sellingStatus[timeLeft]}] {price:>5.2f}$ - {title}</code>
                    </summary>
                    <img src="{galleryURL}"/>
                    <details>
                        <summary>json</summary>
                        <pre>{json}</pre>
                    </details>            
                </details>
                '''.format(**i)
        return html    
    except Exception as e:
        return str(locals())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ['PORT'])