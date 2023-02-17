import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.common import config

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