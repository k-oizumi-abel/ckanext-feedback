from ckan.model.package import Package
from ckan.model.resource import Resource
from sqlalchemy.orm import Session

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
