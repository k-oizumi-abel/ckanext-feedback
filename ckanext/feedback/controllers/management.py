from ckan.common import request
from ckan.plugins import toolkit
from flask import redirect, url_for
import ckanext.feedback.services.utilization.details as detail_service


class ManagementController:
    # management/comments.html
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

    @staticmethod
    def approve_bulk_utilization_comment():
        print(request.form)
        return redirect(url_for('management.comments'))

    @staticmethod
    def approve_bulk_resource_comment():
        print(request.form)
        return redirect(url_for('management.comments'))

    @staticmethod
    def delete_bulk_utilization_comment():
        print(request.form)
        return redirect(url_for('management.comments'))

    @staticmethod
    def delete_bulk_resource_comment():
        print(request.form)
        return redirect(url_for('management.comments'))
