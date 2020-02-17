from flask import request
from flask_jwt_extended import jwt_required

from sqlalchemy import text
import microblog.commons.errors as err
from microblog.api.schemas import PostInfoSchema, PostCreateSchema
from microblog.commons.exceptions import ServiceError
from microblog.commons.helpers import wrap_envelope
from microblog.commons.decorators import get_user_uli
from microblog.commons.pagination import paginate
from microblog.extensions import db
from microblog.models import Post
from .base import BaseResource

class RatingView(BaseResource):
    """Ratings resource"""
    param_2_interval = {'24h': '24 hours',
                        '1h': '1 hour'}

    @jwt_required
    def get(self):
        interval = self.param_2_interval.get(request.args['interval'], '24 hours')

        text_query = text("""
        select max(total_lines), author_id
            from (
                select count(*) as total_lines, author_id
                from (
                    SELECT author_id,
                           timestamp - LAG(timestamp, 1) OVER (PARTITION BY author_id order by timestamp) as time_between,
                           timestamp
                    FROM posts
                    ) as part_table
                group by author_id, time_between is null or time_between < interval '{0}'
                ) as row_num
            group by author_id;
        """.format(interval))
        data = db.session.execute(text_query).fetchall()
        print(wrap_envelope(data))
        # return wrap_envelope(data)
