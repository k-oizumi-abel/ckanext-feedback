from ckan.common import _, c, request
from ckan.lib import helpers
from ckan.plugins import toolkit
from flask import redirect, url_for
import ckanext.feedback.services.utilization.details as detail_service
from ckanext.feedback.models.session import session
import logging


log = logging.getLogger(__name__)


class ManagementController:
    # management/comments
    @staticmethod
    def comments():
        categories = detail_service.get_utilization_comment_categories()
        utilization_comments = detail_service.get_utilization_comments()
        return toolkit.render(
            'management/comments.html',
            {
                'categories': categories,
                'utilization_comments': utilization_comments
            },
        )

    # management/approve_bulk_utilization_comments
    @staticmethod
    def approve_bulk_utilization_comments():
        comments = request.form.getlist('utilization-comments-checkbox')
        if comments:
            detail_service.approve_utilization_comments(comments, c.userobj.id)
            session.commit()
            helpers.flash_success(
                _(
                    f'{len(comments)} bulk approval completed.'
                ),
                allow_html=True,
            )
        return redirect(url_for('management.comments'))

    # management/approve_bulk_resource_comments
    @staticmethod
    def approve_bulk_resource_comments():
        return redirect(url_for('management.comments'))

    # management/delete_bulk_utilization_comments
    @staticmethod
    def delete_bulk_utilization_comments():
        comments = request.form.getlist('utilization-comments-checkbox')
        if comments:
            detail_service.delete_utilization_comments(comments)
            session.commit()
            helpers.flash_success(
                _(
                    f'{len(comments)} bulk delete completed.'
                ),
                allow_html=True,
            )
        return redirect(url_for('management.comments'))

    # management/delete_bulk_resource_comments
    @staticmethod
    def delete_bulk_resource_comments():
        log.info(request.form)
        return redirect(url_for('management.comments'))
