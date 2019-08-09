import os,json,re,traceback
from flask import Flask, jsonify, request, render_template
from ebaysdk.finding import Connection
from datetime import datetime, timedelta

app = Flask(__name__)
ire = re.compile('P(?P<days>[0-9]+)DT(?P<hours>[0-9]+)H(?P<minutes>[0-9]+)M(?P<seconds>[0-9]+)S')

@app.route('/')
def index():
    error = "error"
    try:
        price = float(request.values.get('p',15))
        diff = timedelta(hours=float(request.values.get('h',8)))
        datetime.now()+diff
        d = datetime.now()+diff
        items = []
        api_request = dict(
            itemFilter=[
                {'name': 'Currency', 'value':'USD'},
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'Seller', 'value': os.environ['SELLERS'].split(' ')},
                {'name': 'MaxPrice', 'value': price },
                {'name': 'EndTimeTo',   'value': d.isoformat()}
            ],
            paginationInput=dict(entriesPerPage=20),
            sortOrder='EndTimeSoonest',
            outputSelector=['SellerInfo','PictureURLSuperSize','PictureURLLarge']
        )
        res = Connection(appid=os.environ['EBAY'], config_file=None).execute('findItemsAdvanced', api_request).dict()
        if 'item' in res['searchResult']:
            for i in res['searchResult']['item']:
                i['price']=float(i['sellingStatus']['currentPrice']['value'])+float(i['shippingInfo']['shippingServiceCost']['value'])
                if i['price']>price:
                    continue
                i['imgs'] = [ i[n] for n in ['pictureURLSuperSize','pictureURLLarge','galleryPlusPictureURL','galleryURL'] if n in i]
                i['json']=json.dumps(i,indent=4)
                m = ire.match(i['sellingStatus']['timeLeft'])
                if m:
                    i['diff'] = timedelta(**{k:int(v) for k,v in m.groupdict().items()})
                items.append(i)
        error = None
    except Exception as e:
        error = traceback.format_exc()
    return render_template('index.html',**locals())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ['PORT'])