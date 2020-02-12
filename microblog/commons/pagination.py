"""Simple helper to paginate query
"""
from flask import url_for, request
from sqlalchemy import desc, asc
import logging

from microblog.commons.helpers import wrap_envelope


logger = logging.getLogger(__name__)


DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1
DEFAULT_SORT_DIR = desc
DEFAULT_SORT_BY = 'id'


def paginate(query, schema):
    try:
        page = int(request.args.get('page'))
    except (TypeError, ValueError):
        page = DEFAULT_PAGE_NUMBER

    try:
        per_page = int(request.args.get('page_size'))
    except (TypeError, ValueError):
        per_page = DEFAULT_PAGE_SIZE

    sort_by = request.args.get('sort_by', DEFAULT_SORT_BY)
    sort_dir = request.args.get('sort_dir', DEFAULT_SORT_DIR)
    if type(sort_dir) is str:
        sort_dir = asc if sort_dir == 'asc' else desc if sort_dir == 'desc' else DEFAULT_SORT_DIR

    page_obj = query.order_by(sort_dir(sort_by)).paginate(page=page, per_page=per_page)
    next = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        page_size=per_page,
        **request.view_args
    )
    prev = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        page_size=per_page,
        **request.view_args
    )

    return wrap_envelope({
        'total': page_obj.total,
        'pages': page_obj.pages,
        'next': next,
        'prev': prev,
        'results': schema.dump(page_obj.items).data
        })
