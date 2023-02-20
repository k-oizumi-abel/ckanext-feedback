import logging
import uuid
import datetime
from sqlalchemy.orm import Session
from six import text_type
from sqlalchemy import func
from psycopg2.errors import UndefinedTable
from sqlalchemy.exc import ProgrammingError

from ckanext.feedback.models.download import DownloadSummary
import ckan.plugins.toolkit as tk
from ckan.model import Resource

session = Session()
log = logging.getLogger(__name__)

def get_package_download_count(target_package_id):
    try:
        package_download_count = (
        session.query(Resource.package_id, func.sum(DownloadSummary.download).label('package_download'))
        .join(DownloadSummary, Resource.id == DownloadSummary.resource_id)
        .group_by(Resource.package_id)
        .filter(Resource.package_id == target_package_id)
        .first()
        )
    except ProgrammingError:
        log.error('download_summary table does not exit. Please hit "feedback init" command')
    except Exception as e:
        tk.error_shout(e)

    if package_download_count is None:
            return 0

    return package_download_count.package_download


def get_resource_download_count(target_resource_id):
    try:
        resource_download_count = (
            session.query(DownloadSummary.download)
            .filter_by(resource_id=target_resource_id)
            .scalar()
        )
        return resource_download_count    
    except ProgrammingError:
        log.error('download_summary table does not exit. Please hit "feedback init" command')
    except Exception as e:
        tk.error_shout(e)


def increase_resource_download_count(target_resource_id):
    try:
        resource = session.query(DownloadSummary).filter_by(resource_id=target_resource_id).first()
        if resource is None:
            download_summary_id = text_type(uuid.uuid4())
            resource_download_summary = DownloadSummary(
                download_summary_id,
                target_resource_id,
                1,
                datetime.datetime.now(),
                datetime.datetime.now()
                )
            session.add(resource_download_summary)
        else:
            resource.download = resource.download + 1
            resource.updated = datetime.datetime.now()
        session.commit()        
    except ProgrammingError:
        log.error('download_summary table does not exit. Please hit "feedback init" command')
    except Exception as e:
        tk.error_shout(e)
