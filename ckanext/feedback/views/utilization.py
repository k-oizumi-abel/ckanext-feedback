from flask import Blueprint

import ckanext.feedback.controllers.utilization as utilization

utilization_blueprint = Blueprint('utilization', __name__, url_prefix=u'/utilization')

# Add target page URLs to rules and add each URL to the blueprint
rules = [
    (
        '/details',
        'details',
        utilization.UtilizationController.details,
    ),
    (
        '/registration',
        'registration',
        utilization.UtilizationController.registration,
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
    ('/search', 'search', utilization.UtilizationController.search),
]
for rule in rules:
    utilization_blueprint.add_url_rule(*rule)
