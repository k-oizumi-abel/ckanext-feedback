from datetime import datetime

from ckan.model.package import Package
from ckan.model.resource import Resource

from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import (
    UtilizationComment,
)


# Approve selected utilization comments
def approve_utilization_comments(comment_id_list, approval_user_id):
    session.bulk_update_mappings(
        UtilizationComment,
        [
            {
                'id': comment_id,
                'approval': True,
                'approved': datetime.now(),
                'approval_user_id': approval_user_id,
            }
            for comment_id in comment_id_list
        ],
    )


# Delete selected utilization comments
def delete_utilization_comments(comment_id_list):
    session.query(UtilizationComment).filter(
        UtilizationComment.id.in_(comment_id_list)
    ).delete(synchronize_session='fetch')
