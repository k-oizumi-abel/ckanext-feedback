from datetime import datetime

from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import UtilizationSummary


# Create new utilizaton summary
def create_utilization_summary(resource_id):
    summary = (
        session.query(UtilizationSummary)
        .filter(UtilizationSummary.resource_id == resource_id)
        .first()
    )
    if summary is None:
        summary = UtilizationSummary(
            resource_id=resource_id,
        )
        session.add(summary)


# Increment utilization summary utilization count
def increment_utilization_summary_utilizations(resource_id):
    summary = (
        session.query(UtilizationSummary)
        .filter(UtilizationSummary.resource_id == resource_id)
        .first()
    )
    if summary is None:
        summary = UtilizationSummary(
            resource_id=resource_id,
            utilization=1,
        )
        session.add(summary)
    else:
        summary.utilization = summary.utilization + 1
        summary.updated = datetime.now()


# Increment utilization summary comment count
def increment_utilization_summary_comments(resource_id):
    summary = (
        session.query(UtilizationSummary)
        .filter(UtilizationSummary.resource_id == resource_id)
        .first()
    )
    if summary is None:
        summary = UtilizationSummary(
            resource_id=resource_id,
            comment=1,
        )
        session.add(summary)
    else:
        summary.comment = summary.comment + 1
        summary.updated = datetime.now()
