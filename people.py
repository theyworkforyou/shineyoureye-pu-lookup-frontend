from __future__ import unicode_literals, print_function, absolute_import

from collections import defaultdict

from everypolitician import EveryPolitician


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
