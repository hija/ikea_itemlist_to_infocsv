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

def _parse_id(idstr):
    """
    Converts an id string, e.g. 12345678, to the IKEA item id format, e.g. 123.456.78
    """
    p1 = idstr[0:3]
    p2 = idstr[3:6]
    p3 = idstr[6:]
    return f'{p1}.{p2}.{p3}'

def _parse_product(itemjson, debug_attributes = False):
    """
    Parses the json of a product into a condensed, relevant-information-only dictionary with consistent naming
    """
    attributejson = itemjson['attributes']
    if debug_attributes:
        pprint.pprint(attributejson)
    info_dict = {'product_name': f"{attributejson['name']} {attributejson['type_name']}",
                'product_category': _parse_multi_property(attributejson['catalog_name']),
                'product_price': attributejson['price'],
                'product_color': attributejson['valid_design_text'], #_parse_multi_property(attributejson['color_name']),
                'product_id': _parse_id(attributejson['id']),
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

if __name__ == '__main__':
    pprint.pprint(get_product_info('002.638.50'))
