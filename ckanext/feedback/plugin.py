from ckan import plugins
from ckan.common import config
from ckan.plugins import toolkit
from ckanext.feedback.command import feedback
from ckanext.feedback.services.download import summary as summary_service
from ckanext.feedback.views import download


class FeedbackPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('assets', 'feedback')

    # IClick

    def get_commands(self):
        return [feedback.feedback]

    # IBlueprint

    def get_blueprint(self):
        blueprints = []
        blueprints.append(download.get_download_blueprint())
        return blueprints

    # Check production.ini settings
    # Enable/disable the download module
    def is_enabled_downloads(self):
        return toolkit.asbool(config.get('ckan.feedback.downloads.enable', False))

    # Enable/disable the resources module
    def is_enabled_resources(self):
        return toolkit.asbool(config.get('ckan.feedback.resources.enable', False))

    # Enable/disable the utilizations module
    def is_enabled_utilizations(self):
        return toolkit.asbool(config.get('ckan.feedback.utilizations.enable', False))

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'is_enabled_downloads': self.is_enabled_downloads(),
            'is_enabled_resources': self.is_enabled_resources(),
            'is_enabled_utilizations': self.is_enabled_utilizations(),
            'get_resource_downloads': summary_service.get_resource_downloads,
            'get_package_downloads': summary_service.get_package_downloads,
        }
