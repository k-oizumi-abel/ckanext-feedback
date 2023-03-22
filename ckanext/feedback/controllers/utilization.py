from ckan.common import c, request
from ckan.lib import helpers
from ckan.plugins import toolkit
from flask import redirect, url_for

import ckanext.feedback.services.utilization.details as detail_service
import ckanext.feedback.services.utilization.registration as registration_service
import ckanext.feedback.services.utilization.search as search_service
import ckanext.feedback.services.utilization.summary as summary_service
from ckanext.feedback.models.session import session


class UtilizationController:
    # Render HTML pages
    # utilization/search
    @staticmethod
    def search():
        id = request.args.get('id', '')
        keyword = request.args.get('keyword', '')
        approval = None
        if c.userobj is None or c.userobj.sysadmin is None:
            approval = True
        disable_keyword = request.args.get('disable_keyword', '')
        utilizations = search_service.get_utilizations(id, keyword, approval)

        return toolkit.render(
            'utilization/search.html',
            {
                'keyword': keyword,
                'disable_keyword': disable_keyword,
                'utilizations': utilizations,
            },
        )

    # utilization/new
    @staticmethod
    def new():
        resource_id = request.args.get('resource_id', '')
        return_to_resource = request.args.get('return_to_resource', False)
        resource_details = registration_service.get_resource_details(resource_id)

        return toolkit.render(
            'utilization/new.html',
            {
                'return_to_resource': return_to_resource,
                'resource_details': resource_details,
            },
        )

    # utilization/new
    @staticmethod
    def create():
        message = request.form.get('message', '')
        package_name = request.form.get('package_name', '')
        resource_id = request.form.get('resource_id', '')
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        return_to_resource = eval(request.form.get('return_to_resource'))
        registration_service.create_utilization(resource_id, title, description)
        summary_service.create_utilization_summary(resource_id)
        session.commit()

        helpers.flash_success(message, allow_html=True)

        if return_to_resource:
            return redirect(
                url_for('resource.read', id=package_name, resource_id=resource_id)
            )
        else:
            return redirect(url_for('dataset.read', id=package_name))

    # utilization/<utilization_id>
    @staticmethod
    def details(utilization_id):
        approval = None
        if c.userobj is None or c.userobj.sysadmin is None:
            approval = True
        utilization = detail_service.get_utilization(utilization_id)
        comments = detail_service.get_utilization_comments(utilization_id, approval)
        approved_comments = detail_service.get_approved_utilization_comment_count(
            utilization_id, True
        )
        categories = detail_service.get_utilization_comment_categories()

        return toolkit.render(
            'utilization/details.html',
            {
                'utilization_id': utilization_id,
                'utilization': utilization,
                'comments': comments,
                'approved_comments': approved_comments,
                'categories': categories,
            },
        )

    # utilization/<utilization_id>/approve
    @staticmethod
    def approve(utilization_id):
        resource_id = detail_service.get_utilization(utilization_id).resource_id
        detail_service.approve_utilization(utilization_id, c.userobj.id)
        summary_service.increment_utilization_summary_utilizations(resource_id)
        session.commit()

        return redirect(url_for('utilization.details', utilization_id=utilization_id))

    # utilization/<utilization_id>/comment/new
    @staticmethod
    def create_comment(utilization_id):
        category = request.form.get('category', '')
        content = request.form.get('content', '')
        detail_service.create_utilization_comment(utilization_id, category, content)
        session.commit()

        return redirect(url_for('utilization.details', utilization_id=utilization_id))

    # utilization/<utilization_id>/comment/<comment_id>/approve
    @staticmethod
    def approve_comment(utilization_id, comment_id):
        resource_id = detail_service.get_utilization(utilization_id).resource_id
        detail_service.approve_utilization_comment(comment_id, c.userobj.id)
        summary_service.increment_utilization_summary_comments(resource_id)
        session.commit()

        return redirect(url_for('utilization.details', utilization_id=utilization_id))

    # utilization/comment.html
    @staticmethod
    def comment():
        return toolkit.render('utilization/comment.html')

    # utilization/comment_approval.html
    @staticmethod
    def comment_approval():
        return toolkit.render('utilization/comment_approval.html')
