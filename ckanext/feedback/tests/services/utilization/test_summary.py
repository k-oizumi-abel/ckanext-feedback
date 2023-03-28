import pytest
from ckan import model
from ckan.tests import factories

from ckanext.feedback.command.feedback import (
    create_download_tables,
    create_resource_tables,
    create_utilization_tables,
    get_engine,
)
from ckanext.feedback.models.issue import IssueResolutionSummary
from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import Utilization
from ckanext.feedback.services.utilization.summary import (
    get_package_issue_resolutions,
    get_resource_issue_resolutions,
    increment_issue_resolution_summary,
)


def get_registered_utilization(resource_id):
    return (
        session.query(
            Utilization.id,
        )
        .filter(Utilization.resource_id == resource_id)
        .first()
    )


def get_issue_resolutions(utilization_id):
    count = (
        session.query(IssueResolutionSummary.issue_resolution)
        .filter(IssueResolutionSummary.utilization_id == utilization_id)
        .scalar()
    )
    return count


@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestUtilizationSummaryServices:
    model.repo.init_db()
    engine = get_engine('db', '5432', 'ckan_test', 'ckan', 'ckan')
    create_utilization_tables(engine)
    create_resource_tables(engine)
    create_download_tables(engine)

    def test_increment_issue_resolution_summary(self):
        resource = factories.Resource()
        session.add(
            Utilization(
                resource_id=resource['id'],
                title='test_utilization',
                description='test_utilization_description',
            )
        )
        registered_utilization = get_registered_utilization(resource['id'])

        increment_issue_resolution_summary(registered_utilization.id)
        assert get_issue_resolutions(registered_utilization.id) == 1
        increment_issue_resolution_summary(registered_utilization.id)
        assert get_issue_resolutions(registered_utilization.id) == 2

    def test_get_package_issue_resolutions(self):
        resource = factories.Resource()
        session.add(
            Utilization(
                resource_id=resource['id'],
                title='test_utilization',
                description='test_utilization_description',
            )
        )
        registered_utilization = get_registered_utilization(resource['id'])
        assert get_package_issue_resolutions(resource['package_id']) == 0
        issue_resolution_summary = IssueResolutionSummary(
            utilization_id=registered_utilization.id,
            issue_resolution=1,
            created='2023-03-31 01:23:45.123456',
            updated='2023-03-31 01:23:45.123456',
        )
        session.add(issue_resolution_summary)
        assert get_package_issue_resolutions(resource['package_id']) == 1

    def test_get_resource_issue_resolutions(self):
        resource = factories.Resource()
        session.add(
            Utilization(
                resource_id=resource['id'],
                title='test_utilization',
                description='test_utilization_description',
            )
        )
        registered_utilization = get_registered_utilization(resource['id'])
        assert get_resource_issue_resolutions(resource['id']) == 0
        issue_resolution_summary = IssueResolutionSummary(
            utilization_id=registered_utilization.id,
            issue_resolution=1,
            created='2023-03-31 01:23:45.123456',
            updated='2023-03-31 01:23:45.123456',
        )
        session.add(issue_resolution_summary)
        assert get_resource_issue_resolutions(resource['id']) == 1
