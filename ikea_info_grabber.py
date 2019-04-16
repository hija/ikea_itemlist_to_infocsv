import requests
import pprint

def _parse_product(itemjson):
    pass

def get_product_info(itemcode, market='DE'):
    requests_parameters = {'market': market, 'arg.search_prefix': itemcode, 'arg.filter': f"market:'{market}'"}
    rq = requests.get('https://w102a21be.api.esales.apptus.cloud/api/v1/panels/instant-search', params=requests_parameters)
    rq_response_json = rq.json()
    pprint.pprint(rq_response_json)

get_product_info('502.846.47')
