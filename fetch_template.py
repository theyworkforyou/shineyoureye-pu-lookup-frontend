from __future__ import unicode_literals, print_function, absolute_import

import re

from bs4 import BeautifulSoup
import requests
from six.moves.urllib_parse import urlsplit, urljoin


def rewrite_url(url, real_site_url):
    split_url = urlsplit(url)
    if split_url.scheme or split_url.netloc:
        return url
    if split_url.path == '#':
        return url
    # Otherwise, insert the real site's URL at the start:
    return urljoin(real_site_url, url)


def get_template_from(template_url, real_site_url):
    # Get a URL from the real site which is designed to be easily
    # tranformable into a working Jinja2 template:

    response = requests.get(template_url)

    # Strip out stray ERB tags:
    raw_template_html = response.text
    raw_template_html = re.sub(r'{%\s+(if\s+)?jekyll.*?%}', '', raw_template_html)
    raw_template_html = re.sub(r'{%\s+endif\s+%}', '', raw_template_html)
    raw_template_html = re.sub(r'{% include breadcrumbs.html %}', '', raw_template_html)
    raw_template_html = re.sub(r'{% google_analytics %}', '', raw_template_html)
    raw_template_html = re.sub(r'{% facebook_javascript_sdk %}', '', raw_template_html)

    # soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(raw_template_html, 'html5lib')

    attributes_to_rewrite = [
        ('a', 'href'),
        ('img', 'src'),
        ('link', 'href'),
        ('script', 'src'),
       ]

    for element_name, attribute in attributes_to_rewrite:
        for e in soup.find_all(element_name):
            if e.has_attr(attribute):
                e[attribute] = rewrite_url(e[attribute], real_site_url)

    return soup.prettify()
