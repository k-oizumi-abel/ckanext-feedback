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
    def __init__(self, id, resource_id, download, created, updated):
        self.id = id
        self.resource_id = resource_id
        self.download = download
        self.created = created
        self.updated = updated


meta.mapper(DownloadSummary, download_summary)
