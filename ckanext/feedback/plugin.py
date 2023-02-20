import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckan.common import config
from flask import Blueprint

import ckanext.feedback.services.download.summary as summaryService
from ckanext.feedback.custom_download import custom_download

from ckanext.feedback.command import feedback

class FeedbackPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IClick)
    p.implements(p.IBlueprint)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')
        tk.add_resource('fanstatic', 'feedback')

    def get_blueprint(self):
        blueprint = Blueprint(
                  'download',
                  self.__module__,
                  url_prefix='/dataset/<id>/resource',
                  url_defaults={'package_type': 'dataset'}
              )
        blueprint.add_url_rule('/<resource_id>/download/<filename>', view_func=custom_download)
        blueprint.add_url_rule('/<resource_id>/download', view_func=custom_download)
        return blueprint

    def get_commands(self):
        return [feedback.feedback]

    def show_package_download(self):
        return tk.asbool(config.get(
            "ckan.feedback.download.xxx", False))

    def show_resource_download(seld):
        return tk.asbool(config.get(
            "ckan.feedback.download.yyy", False))

    def get_helpers(self):
        return {
            "show_package_download": FeedbackPlugin.show_package_download,
            "show_resource_download": FeedbackPlugin.show_resource_download,
            "get_resource_download_count": summaryService.get_resource_download_count,
            "get_package_download_count": summaryService.get_package_download_count
        }
