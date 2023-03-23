from ckan.plugins import toolkit
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
                'utilization_commnets': utilization_comments
            },
        )
