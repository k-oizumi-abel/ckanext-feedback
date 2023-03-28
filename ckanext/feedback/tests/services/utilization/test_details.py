import pytest
import ckan.tests.factories as factories

from unittest.mock import patch
from datetime import datetime
from ckan import model
from ckanext.feedback.command.feedback import (
    get_engine, create_utilization_tables, create_resource_tables, create_download_tables
)
from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import (
    Utilization,
    UtilizationComment,
    UtilizationCommentCategory,
)
from ckanext.feedback.services.utilization.details import (
    get_utilization,
    approve_utilization
)

def get_registered_utilization(resource_id):
    return (
        session.query(
            Utilization.id,
            Utilization.approval,
            Utilization.approved,
            Utilization.approval_user_id,
        )
        .filter(Utilization.resource_id == resource_id)
        .first()
    )

def get_registered_utilization_comment(utilization_id):
    return (
        session.query(
            UtilizationComment.utilization_id,
            UtilizationComment.category,
            UtilizationComment.content,
        )
        .filter(UtilizationComment.utilization_id == utilization_id)
        .all()
    )

@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestUtilizationDetailsService:
    @classmethod
    def setup_class(cls):
        model.repo.init_db()
        engine = get_engine('db', '5432', 'ckan_test', 'ckan', 'ckan')
        create_utilization_tables(engine)
        create_resource_tables(engine)
        create_download_tables(engine)

    def test_get_utilization(self):
        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset['id'])
        assert get_registered_utilization(resource['id']) is None
        title = 'test title'
        description = 'test description'
        utilization = Utilization(
            resource_id=resource['id'],
            title=title,
            description=description,
        )
        session.add(utilization)
        registered_utilization = get_registered_utilization(resource['id'])
        result = get_utilization(registered_utilization.id)
        fake_utilization = (title, description, False, resource['name'], resource['id'], dataset['name'])
        assert result == fake_utilization

    @pytest.mark.freeze_time(datetime(2000, 1, 2, 3, 4))
    def test_approve_utilization(self):
        dataset = factories.Dataset()
        user = factories.User()
        resource = factories.Resource(package_id=dataset['id'])
        test_datetime = datetime.now()
        title = 'test title'
        description = 'test description'
        utilization = Utilization(
            resource_id=resource['id'],
            title=title,
            description=description,
            approval=False
        )
        session.add(utilization)

        utilization_before_approved = get_registered_utilization(resource['id'])
        approve_utilization(utilization_before_approved.id,user['id'])
        utilization_after_approved = get_registered_utilization(resource['id'])
        assert utilization_after_approved.approval == True
        assert utilization_after_approved.approved == test_datetime
        assert utilization_after_approved.approval_user_id == user['id']

    def test_get_utilization_comment(self):
        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset['id'])
        assert get_registered_utilization(resource['id']) is None
        title = 'test title'
        description = 'test description'
        utilization = Utilization(
            resource_id=resource['id'],
            title=title,
            description=description,
        )
        session.add(utilization)
        registered_utilization = get_registered_utilization(resource['id'])

        category = UtilizationCommentCategory.REQUEST
        content = 'test content'
        utilization_comment = UtilizationComment(
            utilization_id=registered_utilization.id,
            category=category,
            content=content,
        )
        session.add(utilization_comment)
        registered_utilization_comment = get_registered_utilization_comment(registered_utilization.id)
        assert registered_utilization_comment[0].category == UtilizationCommentCategory.REQUEST
        assert registered_utilization_comment[0].content == content