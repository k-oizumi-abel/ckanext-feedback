from datetime import datetime

from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import (
    Utilization,
    UtilizationComment,
    UtilizationSummary,
)


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


# Recalculate approved utilization and comments related to the utilization summary
def refresh_utilization_summary(resource_id):
    approved_utilizations = (
        session.query(Utilization)
        .filter(
            Utilization.resource_id == resource_id,
            Utilization.approval,
        )
        .count()
    )
    approved_comments = (
        session.query(UtilizationComment)
        .join(Utilization)
        .filter(
            Utilization.resource_id == resource_id,
            UtilizationComment.approval,
        )
        .count()
    )
    summary = (
        session.query(UtilizationSummary)
        .filter(UtilizationSummary.resource_id == resource_id)
        .first()
    )
    if summary is None:
        summary = UtilizationSummary(
            resource_id=resource_id,
            utilization=approved_utilizations,
            comment=approved_comments,
        )
        session.add(summary)
    else:
        summary.utilization = approved_utilizations
        summary.comment = approved_comments
        summary.updated = datetime.now()
