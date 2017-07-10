from __future__ import unicode_literals, print_function, absolute_import

from collections import defaultdict
import csv

from everypolitician import EveryPolitician
import requests
from six.moves.urllib_parse import urljoin


def get_id_to_slug_mapping(real_site_url):
    url = urljoin(real_site_url, '/ids-and-slugs.csv')
    print("Getting the slug <-> id mapping from: {0}".format(url))
    r = requests.get(url)
    reader = csv.DictReader(r.iter_lines())
    return {
        row['id']: row['slug'] for row in reader
    }


def build_rep_lookup():
    result = defaultdict(set)
    ep = EveryPolitician()
    nigeria = ep.country('Nigeria')
    for lname in ('Senate', 'Representatives'):
        popolo = nigeria.legislature(lname).popolo()
        term = popolo.latest_term
        for membership in term.memberships:
            result[membership.area_id] = membership
    return result
