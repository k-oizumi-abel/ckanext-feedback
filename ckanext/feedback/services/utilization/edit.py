from ckan.model.package import Package
from ckan.model.resource import Resource
from sqlalchemy import delete, update
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


# Update utilization
def update_utilization(utilization_id, title, description):
    try:
        session.execute(
            update(Utilization)
            .where(Utilization.id == utilization_id)
            .values(
                title=title,
                description=description,
            )
        )
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


# Delete utilization
def delete_utilization(utilization_id):
    try:
        session.execute(
            delete(Utilization)
            .where(Utilization.id == utilization_id)
        )
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
