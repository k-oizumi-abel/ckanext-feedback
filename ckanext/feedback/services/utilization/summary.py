from datetime import datetime

from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import UtilizationSummary


# Increment utilization summary comment count
def increment_utilization_summary(resource_id):
    summary = session.query(UtilizationSummary).get(resource_id)
    if summary is None:
        summary = UtilizationSummary(
            resource_id=resource_id,
            comment=1,
        )
        session.add(summary)
    else:
        summary.comment = summary.comment + 1
        summary.updated = datetime.now()
