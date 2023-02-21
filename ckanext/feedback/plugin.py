from ckan import plugins
from ckan.common import config
from ckan.plugins import toolkit
from flask import Blueprint
from ckanext.feedback.command import feedback
from ckanext.feedback.custom_download import custom_download
from ckanext.feedback.services.download import summary as summaryService

class FeedbackPlugin(plugins.SingletonPlugin):
    '''
    override update_config
    Called by load_environment at the earliest point that config is available to plugins.
    The config should be updated in place.
    '''
    plugins.implements(plugins.IConfigurer)
    '''
    override get_commands
    Return a list of command functions objects to be registered by the click.add_command
    '''
    plugins.implements(plugins.IClick)
    '''
    override get_blueprint
    Return either a single Flask Blueprint object or a list of Flask
    Blueprint objects to be registered by the app.
    '''
    plugins.implements(plugins.IBlueprint)
    '''
    override get_helpers
    Return a dict mapping names to helper functions
    '''
    plugins.implements(plugins.ITemplateHelpers)


    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'feedback')

    def get_commands(self):
        return [feedback.feedback]

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
    
    def get_helpers(self):
        return {
            "show_package_download": FeedbackPlugin.show_package_download,
            "show_resource_download": FeedbackPlugin.show_resource_download,
            "get_resource_downloads": summaryService.get_resource_downloads,
            "get_package_downloads": summaryService.get_package_downloads
        }

    def show_package_download(self):
        return toolkit.asbool(config.get(
            "ckan.feedback.download.show_package_download", False))

    def show_resource_download(seld):
        return toolkit.asbool(config.get(
            "ckan.feedback.download.show_resource_download", False))
