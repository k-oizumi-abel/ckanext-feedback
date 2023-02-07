import ckan.plugins as p
import ckan.plugins.toolkit as tk
from flask import Blueprint
from ckan.config.routing import SubMapper

from ckanext.feedback.command import feedback

# Render HTML pages
# utilization/details.html
def details():
    return tk.render('utilization/details.html')

# utilization/registration.html
def registration():
    return tk.render('utilization/registration.html')

# utilization/review_approval.html
def review_approval():
    return tk.render('utilization/review_approval.html')

# utilization/review.html
def review():
    return tk.render('utilization/review.html')

# utilization/search.html
def search():
    return tk.render('utilization/search.html')

class FeedbackPlugin(p.SingletonPlugin):
    # Declare that this class implements IConfigurer
    p.implements(p.IConfigurer)
    p.implements(p.IClick)
    p.implements(p.IBlueprint)

    def update_config(self, config):
        
        # Retrieve the value for the "ckan.feedback.substitute_templates" setting from the Config file (/etc/ckan/production.ini) and return it as a bool
        # If the "ckan.feedback.substitute_templates" setting doesn't exist return False
        substitute_templates = tk.asbool(config.get('ckan.feedback.substitute_templates', False))

        # If substitute_templates is True, add the feedback directories below to CKAN's extra paths
        if substitute_templates:
            # Add this plugin's directories to CKAN's extra paths, so that CKAN will use this plugin's custom files.
            # Paths are relative to this plugin.py file.
            tk.add_template_directory(config, 'templates')
            tk.add_public_directory(config, 'public')
            tk.add_resource('assets', 'feedback')

    # Return a flask Blueprint object to be registered by the extension
    def get_blueprint(self):
        blueprint = Blueprint('search', self.__module__)
        # Add target page URLs to rules and add each URL to the blueprint
        rules = [
            ('/utilization/details', 'details', details),
            ('/utilization/registration', 'registration', registration),
            ('/utilization/review_approval', 'review_approval', review_approval),
            ('/utilization/review', 'review', review),
            ('/utilization/search', 'search', search), ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    def get_commands(self):
        return [feedback.feedback]
