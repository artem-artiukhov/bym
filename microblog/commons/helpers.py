import posixpath
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename

from microblog.commons.constants import (MEDIA_MAPPING)


def unwrap_envelope(data):
    return data['data']


def wrap_envelope(data):
    return {'data': data}


def utc_date_obj_from_ts(timestamp, format_to_str=False):
    """Convert timestamp to UTC Datetime Object."""
    utc_date_obj = datetime.utcfromtimestamp(timestamp)
    if format_to_str:
        return utc_date_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    return utc_date_obj


def generate_s3_filename(filename):
    """Generate unique filename with date prefix and uuid in front of
    original filename."""
    utcnow = datetime.utcnow().strftime('%Y/%m/%d')
    filename = secure_filename(filename)
    return posixpath.join(utcnow, f"{uuid.uuid4()}_{filename}")


def get_media_type(mime_type):
    """Get Media Type mapped to Mime-Type.

    Parameters:
        - `mime_type`: string, file mime-type.

    Return:
        - Media Type enum object or None.
    """
    for media_type, mime_types in MEDIA_MAPPING.items():
        if mime_type in mime_types:
            return media_type
    return None
