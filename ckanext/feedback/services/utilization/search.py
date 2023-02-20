from ckan.common import request
from sqlalchemy.orm import Session

from ckanext.feedback.models.utilization import Utilization

session = Session()


# Get records from the Utilization table
def get_utilizations():
    keyword = request.args.get('keyword')
    if keyword:
        rows = (
            session.query(Utilization)
            .filter(Utilization.title.like(f'%{keyword}%'))
            .all()
        )
    else:
        rows = session.query(Utilization).all()

    return rows
