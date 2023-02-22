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
    def enable_downloads(self):
        return toolkit.asbool(config.get('ckan.feedback.downloads.enable', False))

    # Enable/disable the resources module
    def enable_resources(self):
        return toolkit.asbool(config.get('ckan.feedback.resources.enable', False))

    # Enable/disable the utilizations module
    def enable_utilizations(self):
        return toolkit.asbool(config.get('ckan.feedback.utilizations.enable', False))

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'enable_downloads': self.enable_downloads(),
            'enable_resources': self.enable_resources(),
            'enable_utilizations': self.enable_utilizations(),
            'get_resource_downloads': summary_service.get_resource_downloads,
            'get_package_downloads': summary_service.get_package_downloads,
        }
