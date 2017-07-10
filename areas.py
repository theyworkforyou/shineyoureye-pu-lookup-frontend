from __future__ import unicode_literals, print_function, absolute_import

from collections import defaultdict
import csv
from StringIO import StringIO
import requests

from six.moves.urllib_parse import urljoin

RAW_GH_URL = 'https://raw.githubusercontent.com/theyworkforyou/shineyoureye-sinatra/master/'

def build_area_lookup():
    result = {}
    for area_type in ['FED', 'SEN']:
        result[area_type] = defaultdict(set)
        mapping_url = urljoin(
            RAW_GH_URL,
            'mapit/mapit_to_ep_area_ids_mapping_{0}.csv'.format(area_type))
        print("Loading the area mapping {0}".format(mapping_url))
        csv_data = requests.get(mapping_url).text
        reader = csv.reader(StringIO(csv_data.encode('utf-8')))
        for mapit_id, ep_area_id in reader:
            result[area_type][int(mapit_id)].add(ep_area_id.decode('utf-8'))
    return result
