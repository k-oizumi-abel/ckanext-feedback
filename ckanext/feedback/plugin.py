import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.common import config
from flask import Blueprint

import ckanext.feedback.services.download.summary as summaryService
from ckan.ckan.views.resource import download as alias
from ckan.ckan.views import resource

from ckanext.feedback.command import feedback

class FeedbackPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'feedback')

        def custom_download(package_type, id, resource_id, filename=None):
            summaryService.increase_resource_download_count(resource_id)
            alias(package_type, id, resource_id, filename=None)

        resource.download = custom_download

    def get_blueprint(self):
        blueprint = Blueprint("download", self.__module__)
        return blueprint

    def get_commands(self):
        return [feedback.feedback]

    def show_package_download(self):
        return toolkit.asbool(config.get(
            "ckan.feedback.download.xxx", False))

    def show_resource_download(seld):
        return toolkit.asbool(config.get(
            "ckan.feedback.download.yyy", False))

    def get_helpers(self):
        return {
            "show_package_download": FeedbackPlugin.show_package_download,
            "show_resource_download": FeedbackPlugin.show_resource_download,
            "get_resource_download_count": summaryService.get_resource_download_count
        }