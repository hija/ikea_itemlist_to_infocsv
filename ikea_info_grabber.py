import requests
import pprint

def _parse_product_catergory(catalog_name):
    if '|' in catalog_name:
        # Return only main category, i.e.
        #'Bettsofas & -sessel|Sofas & Polstergruppen' ==> Bettsofas & -sessel
        return catalog_name.split('|')[0].strip()
    else:
        return catalog_name.strip()

def _parse_product(itemjson):
    """
    Parses the json of a product into a condensed, relevant-information-only dictionary with consistent naming
    """
    attributejson = itemjson['attributes']
    info_dict = {'product_name': attributejson['name'],
                'product_category': _parse_product_catergory(attributejson['catalog_name']),
                'product_price': attributejson['price'],
                'product_color': attributejson['color_name'],
                'is_online_sellable': attributejson['online_sellable'],
                'is_family_price': attributejson['is_family_price']}
    return info_dict

def get_product_info(itemcode, market='DE'):
    requests_parameters = {'market': market, 'arg.search_prefix': itemcode, 'arg.filter': f"market:'{market}'"}
    rq = requests.get('https://w102a21be.api.esales.apptus.cloud/api/v1/panels/instant-search', params=requests_parameters)
    rq_response_json = rq.json()

    for product in rq_response_json['productSuggestions'][0]['products']:
        pprint.pprint(_parse_product(product))

get_product_info('502.846.47')
