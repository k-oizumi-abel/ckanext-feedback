import uuid
from datetime import datetime

from ckan.model.package import Package
from ckan.model.resource import Resource
from sqlalchemy import insert, update
from sqlalchemy.orm import Session

from ckanext.feedback.models.utilization import Utilization, UtilizationSummary

session = Session()


# Get details from the Resource record
def get_resource_details(resource_id):
    row = (
        session.query(
            Resource.name.label('resource_name'),
            Resource.id.label('resource_id'),
            Package.name.label('package_name'),
        )
        .join(Package, Package.id == Resource.package_id)
        .filter(Resource.id == resource_id)
        .one()
    )
    return row


# Submit utilization
def submit_utilization(resource_id, title, content):
    utilization_id = str(uuid.uuid4())

    try:
        session.execute(
            insert(Utilization).values(
                id=utilization_id,
                resource_id=resource_id,
                title=title,
                description=content,
                created=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                approval=False,
                approved=None,
                approval_user_id=None,
            )
        )
        session.commit()
        return utilization_id
    except Exception as e:
        session.rollback()
        raise e


# Create utilizaton summary
def create_utilization_summary(resource_id):
    count = (
        session.query(UtilizationSummary.utilization)
        .filter(UtilizationSummary.resource_id == resource_id)
        .first()
    )
    try:
        if count:
            session.execute(
                update(UtilizationSummary)
                .where(UtilizationSummary.resource_id == resource_id)
                .values(
                    utilization=count.utilization + 1,
                    updated=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                )
            )
            session.commit()
        else:
            session.execute(
                insert(UtilizationSummary).values(
                    id=str(uuid.uuid4()),
                    resource_id=resource_id,
                    utilization=1,
                    comment=0,
                    created=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    updated=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                )
            )
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
