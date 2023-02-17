import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.common import config
from flask import Blueprint

import ckanext.feedback.controllers.utilization as utilization
import ckanext.feedback.services.utilization.search as searchService
from ckanext.feedback.command import feedback


class FeedbackPlugin(p.SingletonPlugin):
    # Declare class implements
    p.implements(p.IConfigurer)
    p.implements(p.IClick)
    p.implements(p.IBlueprint)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's directories to CKAN's extra paths, so that
        # CKAN will use this plugin's custom files.
        # Paths are relative to this plugin.py file.
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')
        tk.add_resource('assets', 'feedback')

    # Return a flask Blueprint object to be registered by the extension
    def get_blueprint(self):
        blueprint = Blueprint('search', self.__module__)
        # Add target page URLs to rules and add each URL to the blueprint
        rules = [
            (
                '/utilization/details',
                'details',
                utilization.UtilizationController.details,
            ),
            (
                '/utilization/registration',
                'registration',
                utilization.UtilizationController.registration,
            ),
            (
                '/utilization/comment_approval',
                'comment_approval',
                utilization.UtilizationController.comment_approval,
            ),
            (
                '/utilization/comment',
                'comment',
                utilization.UtilizationController.comment,
            ),
            ('/utilization/search', 'search', utilization.UtilizationController.search),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    def get_commands(self):
        return [feedback.feedback]

    # Check production.ini settings
    # Enable/disable the download module
    def enable_downloads(self):
        return tk.asbool(config.get('ckan.feedback.downloads.enable', False))

    # Enable/disable the resources module
    def enable_resources(self):
        return tk.asbool(config.get('ckan.feedback.resources.enable', False))

    # Enable/disable the utilizations module
    def enable_utilizations(self):
        return tk.asbool(config.get('ckan.feedback.utilizations.enable', False))

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'enable_downloads': FeedbackPlugin.enable_downloads,
            'enable_resources': FeedbackPlugin.enable_resources,
            'enable_utilizations': FeedbackPlugin.enable_utilizations,
            'get_utilizations': searchService.get_utilizations,
            'get_utilizations_count': searchService.get_utilizations_count,
            'keep_keyword': searchService.keep_keyword,
            'get_package_info': searchService.get_package_info,
            'get_resource_info': searchService.get_resource_info,
        }
