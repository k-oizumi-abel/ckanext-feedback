from ckan import plugins
from ckan.common import config
from ckan.plugins import toolkit

from ckanext.feedback.command import feedback
from ckanext.feedback.views.utilization import utilization_blueprint


class FeedbackPlugin(plugins.SingletonPlugin):
    # Declare class implements
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        # Add this plugin's directories to CKAN's extra paths, so that
        # CKAN will use this plugin's custom files.
        # Paths are relative to this plugin.py file.
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('assets', 'feedback')

    # Return a flask Blueprint object to be registered by the extension
    def get_blueprint(self):
        blueprints = []
        blueprints.append(utilization_blueprint)
        return blueprints

    def get_commands(self):
        return [feedback.feedback]

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

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'enable_downloads': self.enable_downloads(),
            'enable_resources': self.enable_resources(),
            'enable_utilizations': self.enable_utilizations(),
        }
