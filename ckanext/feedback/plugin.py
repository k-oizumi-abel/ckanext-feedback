from ckan import plugins
from ckan.common import config
from ckan.plugins import toolkit
from flask import Blueprint
from ckanext.feedback.command import feedback
from ckanext.feedback.controllers.download import DownloadController
from ckanext.feedback.services.download import summary as summaryService
from ckanext.feedback.views.download import blueprint as download_blueprint


class FeedbackPlugin(plugins.SingletonPlugin):
    # Declare class implements
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        # Retrieve the value for the "ckan.feedback.substitute_templates"
        # setting from the Config file (/etc/ckan/production.ini) and
        # return it as a bool.
        # If the "ckan.feedback.substitute_templates" setting doesn't exist
        # return False
        substitute_templates = toolkit.asbool(
            config.get('ckan.feedback.substitute_templates', False)
        )

        # If substitute_templates is True, add the feedback directories below
        # to CKAN's extra paths
        if substitute_templates:
            # Add this plugin's directories to CKAN's extra paths, so that
            # CKAN will use this plugin's custom files.
            # Paths are relative to this plugin.py file.
            toolkit.add_template_directory(config, 'templates')
            toolkit.add_public_directory(config, 'public')
            toolkit.add_resource('fanstatic', 'feedback')

    def get_commands(self):
        return [feedback.feedback]

    # Return a flask Blueprint object to be registered by the extension
    def get_blueprint(self):
#        blueprints = []
#        blueprints.append(download_blueprint)
#        return blueprints
        blueprint = Blueprint(
                  'download',
                  self.__module__,
                  url_prefix='/dataset/<id>/resource',
                  url_defaults={'package_type': 'dataset'}
              )
        blueprint.add_url_rule('/<resource_id>/download/<filename>', view_func=DownloadController.custom_download)
        blueprint.add_url_rule('/<resource_id>/download', view_func=DownloadController.custom_download)
        return blueprint

    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'show_package_downloads': FeedbackPlugin.show_package_downloads,
            'show_resource_downloads': FeedbackPlugin.show_resource_downloads,
            'get_resource_downloads': summaryService.get_resource_downloads,
            'get_package_downloads': summaryService.get_package_downloads,
        }

    # Check production.ini settings
    # Show/hide the sum of resource downloads in the same package
    def show_package_downloads(self):
        return toolkit.asbool(
            config.get('ckan.feedback.download.show_package_downloads', False)
        )
    # Show/hide resource downloads
    def show_resource_downloads(seld):
        return toolkit.asbool(
            config.get('ckan.feedback.download.show_resource_downloads', False)
        )
