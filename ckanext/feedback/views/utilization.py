from flask import Blueprint

from ckanext.feedback.controllers import utilization
from ckanext.feedback.views.error_handler import add_error_handler

blueprint = Blueprint('utilization', __name__, url_prefix='/utilization')

# Add target page URLs to rules and add each URL to the blueprint
rules = [
    ('/search', 'search', utilization.UtilizationController.search),
    ('/new', 'new', utilization.UtilizationController.new, {'methods': ['GET']}),
    ('/new', 'create', utilization.UtilizationController.create, {'methods': ['POST']}),
    (
        '/<utilization_id>',
        'details',
        utilization.UtilizationController.details,
    ),
    (
        '/<utilization_id>/approve',
        'approve',
        utilization.UtilizationController.approve,
        {'methods': ['POST']},
    ),
    (
        '/<utilization_id>/comment/new',
        'create_comment',
        utilization.UtilizationController.create_comment,
        {'methods': ['POST']},
    ),
    (
        '/<utilization_id>/comment/<comment_id>/approve',
        'approve_comment',
        utilization.UtilizationController.approve_comment,
        {'methods': ['POST']},
    ),
    (
        '/comment_approval',
        'comment_approval',
        utilization.UtilizationController.comment_approval,
    ),
    (
        '/comment',
        'comment',
        utilization.UtilizationController.comment,
    ),
]
for rule, endpoint, view_func, *others in rules:
    options = next(iter(others), {})
    blueprint.add_url_rule(rule, endpoint, view_func, **options)


@add_error_handler
def get_utilization_blueprint():
    return blueprint
