import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from six import text_type

from ckanext.feedback.models.download import DownloadSummary
import ckan.plugins.toolkit as tk

session = Session()

# def get_package_download_count(package_id):
#    package_download_count = session.query(Resource, Resource.package_id, func.sum(DownloadSummary.download))
#    .join(DownloadSummary, DownloadSummary.resource_id == Resource.id)
#    .group_by(Resource.package_id)
#    .filter_by(Resource.package_id = package_id)
#    .scalar()
#
#    return package_download_count.download


def get_resource_download_count(target_resource_id):
    resource_download_count = (
        session.query(DownloadSummary.download)
        .filter_by(resource_id=target_resource_id)
        .scalar()
    )

    return resource_download_count


def increase_resource_download_count(target_resource_id):
    try:
        resource = session.query(DownloadSummary).filter_by(resource_id=target_resource_id).first()
        if resource is None:
            download_summary_id = text_type(uuid.uuid4())
            resource_download_summary = DownloadSummary()
            resource_download_summary.id = download_summary_id
            resource_download_summary.resource_id = target_resource_id
            resource_download_summary.download = 1
            resource_download_summary.created = datetime.datetime.now()
            resource_download_summary.updated = datetime.datetime.now()
            session.add(resource_download_summary)
        else:
            resource.download = resource.download + 1
            resource.updated = datetime.datetime.now()
        session.commit()        
    except Exception as e:
        tk.error_shout(e)
