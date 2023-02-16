import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.common import config
from flask import Blueprint  # type: ignore

import ckanext.feedback.controllers.download as download
import ckanext.feedback.services.download.summary as summaryService  # type: ignore

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

    def get_blueprint(self):
        blueprint = Blueprint("download", self.__module__)
        rules = [
            ('/increase/<target_resource_id>', 'increase_resource_download_count', download.DownloadController.increase_resource_download_count),
            ('/download/test', 'test', download.DownloadController.test),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

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
            "get_resource_download_count": summaryService.get_resource_download_count,
            "increase_resource_download_count": summaryService.increase_resource_download_count
        }