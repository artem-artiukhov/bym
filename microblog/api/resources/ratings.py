from flask import request
from flask_jwt_extended import jwt_required

from sqlalchemy import text
from microblog.extensions import db
from microblog.commons.helpers import wrap_envelope
from .base import BaseResource


class RatingView(BaseResource):
    """Ratings resource"""
    param_2_interval = {'24h': ['day', 'days'],
                        '1h': ['hour', 'hours']}

    @jwt_required
    def get(self):
        interval = self.param_2_interval.get(request.args['interval'], ['day', 'days'])

        text_query = text("""
        WITH
            posts AS (
                SELECT date_trunc('{0}', timestamp) as post_date, author_id
                FROM Posts
            ),
            groups AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY post_date) AS rn,
                    post_date - concat(to_char(ROW_NUMBER() OVER (ORDER BY post_date), '999'), ' {1}')::interval as grp,
                    post_date,
                    author_id
                FROM posts
            )

        select max(consecutive_actions) as post_num, author_id, u.email
            from (
                SELECT
                    COUNT(*) AS consecutive_actions,
                    author_id,
                    MIN(post_date) AS min_date,
                    MAX(post_date) AS max_date,
                    grp
                FROM groups
                GROUP BY author_id, grp
                ORDER BY 2, 3) as act
            join users u on u.id = author_id
        group by author_id, u.email
        """.format(interval[0], interval[1]))

        query = db.session.execute(text_query).fetchall()
        return wrap_envelope({'results': [dict(row) for row in query]})
