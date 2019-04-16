import requests
import pprint

def _parse_multi_property(property_element):
    """
    Parses a |-separated property element to a single property using only the first property
    """
    if '|' in property_element:
        # Return only main category, i.e.
        #'Bettsofas & -sessel|Sofas & Polstergruppen' ==> Bettsofas & -sessel
        return property_element.split('|')[0].strip()
    else:
        return property_element.strip()

def _parse_product(itemjson):
    """
    Parses the json of a product into a condensed, relevant-information-only dictionary with consistent naming
    """
    attributejson = itemjson['attributes']
    info_dict = {'product_name': attributejson['name'],
                'product_category': _parse_multi_property(attributejson['catalog_name']),
                'product_price': attributejson['price'],
                'product_color': _parse_multi_property(attributejson['color_name']),
                'is_online_sellable': attributejson['online_sellable'],
                'is_family_price': attributejson['is_family_price']}
    return info_dict

def get_product_info(itemcode, market='DE'):
    """
    Returns a list of dictionaries with each of them containing information about IKEA items
    """
    requests_parameters = {'market': market, 'arg.search_prefix': itemcode, 'arg.filter': f"market:'{market}'"}
    #TODO: Get the search API somewhat more dynamically (not hardcoding), e.g. from IKEA website
    rq = requests.get('https://w102a21be.api.esales.apptus.cloud/api/v1/panels/instant-search', params=requests_parameters)
    rq_response_json = rq.json()

    parsed_products = []
    for product in rq_response_json['productSuggestions'][0]['products']:
        parsed_products.append(_parse_product(product))

    return parsed_products
