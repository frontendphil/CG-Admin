import re

from django.db.models import Q
from django.template import Library

register = Library()


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_natural_range(value):
    return [i + 1 for i in range(value)]


@register.filter
def first5(query_set):
    return query_set[0:5]


@register.filter
def count(query_set):
    return query_set.count()


@register.filter
def chronologic(query_set):
    return query_set.order_by("-date")


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    # Query to search for every search term
    query = None
    terms = normalize_query(query_string)

    for term in terms:
        # Query to search for a given term in each field
        or_query = None

        for field in fields:
            q = Q(**{"%s__icontains" % field: term})

            or_query = or_query | q if not or_query is None else q

        query = query & or_query if not query is None else or_query

    return query
