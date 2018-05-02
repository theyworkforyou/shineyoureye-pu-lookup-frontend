from __future__ import unicode_literals, print_function, absolute_import

from flask import Flask, render_template_string, request
import requests
from six.moves.urllib_parse import quote, urljoin

from fetch_template import get_template_from
from areas import build_area_lookup
from people import build_rep_lookup, get_id_to_slug_mapping

app = Flask(__name__)

REAL_SITE_URL = 'http://www.shineyoureye.org'

TEMPLATE_URL = urljoin(REAL_SITE_URL, '/jinja2-template.html')

# LOOKUP_URL_FORMAT = 'https://pu-lookup.herokuapp.com/?lookup={0}'
LOOKUP_URL_FORMAT = 'https://hfwi7tdz3e.execute-api.eu-west-2.amazonaws.com/dev?lookup={0}'

rewritten_layout_template = get_template_from(TEMPLATE_URL, REAL_SITE_URL)

area_lookup = build_area_lookup()
rep_lookup = build_rep_lookup()
person_id_to_slug = get_id_to_slug_mapping(REAL_SITE_URL)


def membership_and_slug_tuple(membership):
    if membership:
        return (
            membership,
            person_id_to_slug[membership.person.id]
        )
    return (None, None)


def get_memberships(mapit_area_id, mapit_type):
    ep_area_ids = area_lookup[mapit_type].get(mapit_area_id)
    if not ep_area_ids:
        return []
    return [
        membership_and_slug_tuple(rep_lookup.get(ep_area_id))
        for ep_area_id in ep_area_ids
        if ep_area_id in rep_lookup]

def process_results(response):
    result = {}
    result['area'] = response['area']
    result['state'] = response.get('state')
    # FIXME: add governors here...
    # Find MPs:
    result['federal_constituencies'] = response.get('federal_constituencies', [])
    for area in result['federal_constituencies']:
        area['memberships'] = get_memberships(area['id'], 'FED')
    # Find Senators:
    result['senatorial_districts'] = response.get('senatorial_districts', [])
    for area in result['senatorial_districts']:
        area['memberships'] = get_memberships(area['id'], 'SEN')
    return result


@app.route('/')
def homepage():
    return render_template_string(
        rewritten_layout_template,
        content='homepage.html'
    )


@app.route('/lookup', methods=['POST'])
def lookup():
    query = request.form.get('pu-number')
    # Make a query to the PU lookup service:
    response = requests.get(
        LOOKUP_URL_FORMAT.format(quote(query))
    ).json()
    if 'error' in response:
        return render_template_string(
            rewritten_layout_template,
            content='error.html',
            error=response['error']
        )
    return render_template_string(
        rewritten_layout_template,
        content='results.html',
        real_site_url=REAL_SITE_URL,
        **process_results(response)
    )

if __name__ == "__main__":
    app.run()
