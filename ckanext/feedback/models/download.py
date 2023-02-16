import datetime

import ckan.model.domain_object as domain_object
import ckan.model.meta as meta
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Text,
    Integer,
    TIMESTAMP,
)

__all__ = ['download_summary']

download_summary = Table(
    'download_summary',
    meta.metadata,
    Column('id', Text, primary_key=True, nullable=False),
    Column('resource_id', Text, ForeignKey('resource.id'), nullable=False),
    Column('download', Integer),
    Column('created', TIMESTAMP),
    Column('updated', TIMESTAMP),
)


class DownloadSummary(domain_object.DomainObject):
    id: str
    resource_id: str
    download: int
    created: datetime.datetime
    updated: datetime.datetime


meta.mapper(DownloadSummary, download_summary)
