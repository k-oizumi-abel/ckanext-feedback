import uuid
from datetime import datetime

from ckan.model.package import Package
from ckan.model.resource import Resource
from sqlalchemy import insert
from sqlalchemy.orm import Session

from ckanext.feedback.models.utilization import Utilization

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
