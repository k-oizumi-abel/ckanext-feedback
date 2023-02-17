import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from six import text_type
import logging

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
        print("increase function start")
        resource = (
            session.query(DownloadSummary.download, DownloadSummary.updated)
            .filter_by(resource_id=target_resource_id)
            .scalar()
        )
        resource.download = resource.download + 1
        resource.updated = datetime.datetime.now()
        session.commit()
    except NoResultFound:
        print("create new column")
        download_summary_id = text_type(uuid.uuid4())
        session.add(
            DownloadSummary(
                id=download_summary_id,
                resource_id=target_resource_id,
                download=1,
                created=datetime.datetime.now(),
                updated=datetime.datetime.now(),
            )
        )
        session.commit()
    except Exception as e:
        tk.error_shout(e)
