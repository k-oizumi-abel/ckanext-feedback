from ckan.common import request
from ckan.plugins import toolkit
from flask import Flask

import ckanext.feedback.services.utilization.details as detail_service
import ckanext.feedback.services.utilization.registration as registration_service
import ckanext.feedback.services.utilization.search as search_service

app = Flask(__name__)


class UtilizationController:
    # Render HTML pages
    # utilization/details.html
    @app.route('/', methods=['GET', 'POST'])
    def details():
        if request.method == 'POST':
            utilization_id = request.params('utilization_id', '')
            comment_id = request.params('comment_id')
            comment_type = request.params('comment_type', '')
            comment_content = request.params('comment_content', '')
            approval_user = request.params('approval_user')
        else:
            utilization_id = request.args.get('utilization_id', '')
            comment_id = request.args.get('comment_id')
            comment_type = request.args.get('comment_type', '')
            comment_content = request.args.get('comment_content', '')
            approval_user = request.args.get('approval_user')
        submit_comment = detail_service.submit_comment(
            utilization_id, comment_type, comment_content
        )
        submit_approval = detail_service.submit_approval(comment_id, approval_user)
        details = detail_service.get_utilization_details(utilization_id)
        comments = detail_service.get_utilization_comments(utilization_id)

        return toolkit.render(
            'utilization/details.html',
            {
                'utilization_id': utilization_id,
                'details': details,
                'comments': comments,
                'submit_comment': submit_comment,
                'submit_approval': submit_approval,
            },
        )

    # utilization/registration.html
    def registration():
        resource_id = request.args.get('resource_id', '')
        resource_details = registration_service.get_resource_details(resource_id)

        return toolkit.render(
            'utilization/registration.html',
            {
                'resource_details': resource_details,
            },
        )

    # utilization/edit.html
    def edit():
        return toolkit.render('utilization/edit.html')

    # utilization/comment_approval.html
    def comment_approval():
        return toolkit.render('utilization/comment_approval.html')

    # utilization/recommentview.html
    def comment():
        return toolkit.render('utilization/comment.html')

    # utilization/search.html
    def search():
        keyword = request.args.get('keyword', '')
        transitioned = request.args.get('transitioned', '')
        utilizations = search_service.get_utilizations(keyword)
        approved_utilizations = search_service.get_approved_utilizations(keyword)

        return toolkit.render(
            'utilization/search.html',
            {
                'keyword': keyword,
                'transitioned': transitioned,
                'utilizations': utilizations,
                'approved_utilizations': approved_utilizations,
            },
        )
