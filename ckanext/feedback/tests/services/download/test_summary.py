import pytest
from ckan import model
from ckan.tests import factories

from ckanext.feedback.command.feedback import (
    create_download_tables,
    create_resource_tables,
    create_utilization_tables,
    get_engine,
)
from ckanext.feedback.models.download import DownloadSummary
from ckanext.feedback.models.session import session
from ckanext.feedback.services.download.summary import (
    get_package_downloads,
    get_resource_downloads,
    increment_resource_downloads,
)


def get_downloads(resource_id):
    count = (
        session.query(DownloadSummary.download)
        .filter(DownloadSummary.resource_id == resource_id)
        .scalar()
    )
    return count


@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestDownloadServices:
    @classmethod
    def setup_class(cls):
        model.repo.init_db()
        engine = get_engine('db', '5432', 'ckan_test', 'ckan', 'ckan')
        create_utilization_tables(engine)
        create_resource_tables(engine)
        create_download_tables(engine)

    def test_increment_resource_downloads(self):
        resource = factories.Resource()
        increment_resource_downloads(resource['id'])
        assert get_downloads(resource['id']) == 1
        increment_resource_downloads(resource['id'])
        assert get_downloads(resource['id']) == 2

    def test_get_package_download(self):
        resource = factories.Resource()
        assert get_package_downloads(resource['package_id']) == 0
        download_summary = DownloadSummary(
            id=str('test_id'),
            resource_id=resource['id'],
            download=1,
            created='2023-03-31 01:23:45.123456',
            updated='2023-03-31 01:23:45.123456',
        )
        session.add(download_summary)
        assert get_package_downloads(resource['package_id']) == 1

    def test_get_resource_download(self):
        resource = factories.Resource()
        assert get_resource_downloads(resource['id']) == 0
        download_summary = DownloadSummary(
            id=str('test_id'),
            resource_id=resource['id'],
            download=1,
            created='2023-03-31 01:23:45.123456',
            updated='2023-03-31 01:23:45.123456',
        )
        session.add(download_summary)
        assert get_resource_downloads(resource['id']) == 1
