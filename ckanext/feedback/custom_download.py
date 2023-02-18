from ckanext.feedback.services.download.summary import increase_resource_download_count
from ckan.views.resource import download

def custom_download(package_type, id, resource_id, filename=None):
    increase_resource_download_count(resource_id)
    return download(package_type, id, resource_id, filename=filename)