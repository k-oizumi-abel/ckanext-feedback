from datetime import datetime

import pytest
from ckan import model
from ckan.tests import factories

from ckanext.feedback.command.feedback import (
    create_download_tables,
    create_resource_tables,
    create_utilization_tables,
    get_engine,
)
from ckanext.feedback.models.issue import IssueResolution
from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import Utilization
from ckanext.feedback.services.utilization.details import (
    create_issue_resolution,
    get_issue_resolutions,
)


def get_registered_utilization(resource_id):
    return (
        session.query(
            Utilization.id,
        )
        .filter(Utilization.resource_id == resource_id)
        .first()
    )


def get_registered_issue_resolution(utilization_id):
    return (
        session.query(
            IssueResolution.utilization_id,
            IssueResolution.description,
            IssueResolution.creator_user_id,
        )
        .filter(IssueResolution.utilization_id == utilization_id)
        .first()
    )


@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestUtilizationDetailServices:
    model.repo.init_db()
    engine = get_engine('db', '5432', 'ckan_test', 'ckan', 'ckan')
    create_utilization_tables(engine)
    create_resource_tables(engine)
    create_download_tables(engine)

    def test_get_issue_resolutions(self):
        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset['id'])
        user = factories.User()

        session.add(
            Utilization(
                resource_id=resource['id'],
                title='test_utilization',
                description='test_utilization_description',
            )
        )

        registered_utilization = get_registered_utilization(resource['id'])
        assert get_registered_issue_resolution(registered_utilization.id) is None
        description = 'test_issue_resolution_description'
        time = datetime.now()

        session.add(
            IssueResolution(
                utilization_id=registered_utilization.id,
                description=description,
                created=time,
                creator_user_id=user['id'],
            )
        )

        issue_resolution = get_issue_resolutions(registered_utilization.id)[0]

        assert issue_resolution.utilization_id == registered_utilization.id
        assert issue_resolution.description == description
        assert issue_resolution.created == time
        assert issue_resolution.creator_user_id == user['id']

    def test_create_issue_resolution(self):
        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset['id'])
        user = factories.Sysadmin()

        session.add(
            Utilization(
                resource_id=resource['id'],
                title='test_utilization',
                description='test_utilization_description',
            )
        )

        registered_utilization = get_registered_utilization(resource['id'])
        description = 'test_issue_resolution_description'
        create_issue_resolution(registered_utilization.id, description, user['id'])

        issue_resolution = (registered_utilization.id, description, user['id'])

        assert (
            get_registered_issue_resolution(registered_utilization.id)
            == issue_resolution
        )
