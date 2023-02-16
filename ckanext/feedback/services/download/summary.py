import uuid
import sys
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
#
#    package_download_count = 0
#    resource_ids = (
#        session.query(Resource.resource_id)
#        .filter_by(Resource.package_id = package_id)
#        .all()
#    )
#    for resource_id in resource_ids:
#        resource_download_count = (
#            session.query(DownloadSummary.download)
#            .filter_by(DownloadSummary.resource_id = resource_id)
#            .scalar()
#        )
#        package_download_count = package_download_count + resource_download_count
#    return package_download_count


def get_resource_download_count(target_resource_id):
    resource_download_count = (
        session.query(DownloadSummary.download)
        .filter_by(resource_id=target_resource_id)
        .scalar()
    )

    return resource_download_count


def increase_resource_download_count(target_resource_id):
    try:
        resource_download_count = (
            session.query(DownloadSummary.download)
            .filter_by(resource_id=target_resource_id)
            .scalar()
        )
        resource_download_count = resource_download_count + 1
        # TODO: renew updated  
    except NoResultFound:
        # ckan use uuid4
        download_summary_id = text_type(uuid.uuid4())
        # ckan use datetime.datetime.now
        session.add(
            DownloadSummary(
                id=download_summary_id,
                resource_id=target_resource_id,
                download=1,
                created=datetime.datetime.now(),
                updated=datetime.datetime.now(),
            )
        )
    except Exception as e:
        tk.error_shout(e)
        sys.exit(1)

    session.commit()
