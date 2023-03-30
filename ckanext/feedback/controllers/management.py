from ckan.common import _, c, request
from ckan.lib import helpers
from ckan.plugins import toolkit
from flask import redirect, url_for

import ckanext.feedback.services.management.comments as comments_service
import ckanext.feedback.services.utilization.details as detail_service
from ckanext.feedback.models.session import session


class ManagementController:
    # management/comments
    @staticmethod
    def comments():
        categories = detail_service.get_utilization_comment_categories()
        utilization_comments = detail_service.get_utilization_comments()
        return toolkit.render(
            'management/comments.html',
            {'categories': categories, 'utilization_comments': utilization_comments},
        )

    # management/approve_bulk_utilization_comments
    @staticmethod
    def approve_bulk_utilization_comments():
        comments = request.form.getlist('utilization-comments-checkbox')
        if comments:
            utilizations = comments_service.get_utilizations_by_comments(comments)
            comments_service.approve_utilization_comments(comments, c.userobj.id)
            comments_service.refresh_utilizations_comments(utilizations)
            session.commit()
            helpers.flash_success(
                f'{len(comments)} ' + _('bulk approval completed.'),
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
            utilizations = comments_service.get_utilizations_by_comments(comments)
            comments_service.delete_utilization_comments(comments)
            comments_service.refresh_utilizations_comments(utilizations)
            session.commit()

            helpers.flash_success(
                f'{len(comments)} ' + _('bulk delete completed.'),
                allow_html=True,
            )
        return redirect(url_for('management.comments'))

    # management/delete_bulk_resource_comments
    @staticmethod
    def delete_bulk_resource_comments():
        return redirect(url_for('management.comments'))
