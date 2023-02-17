import inspect, imp

from ckan.ckan.views import resource
from ckanext.feedback.services.download.summary import increase_resource_download_count
from resource import download as alias

def custom_download(package_type, id, resource_id, filename=None):
    increase_resource_download_count(resource_id)
    resource.download(package_type, id, resource_id, filename=None)

def hooking():
    frame = [frame for (frame, filename, _, _, _,_) in 
             inspect.getouterframes(inspect.currentframe())[1:] 
                 if not 'importlib' in filename and not __file__ in filename][0]
        # 呼び出しもとの取得、importには、importlibを介している場合がある為
    frame.f_locals['download'] = custom_download

class Importer(object):
    old_import = __import__
    def new_import(self, *args, **kwargs):
        if args[0] == __name__: hooking() 
        return self.old_import(*args, **kwargs)

hooking()
from ckan.ckna.views import resource
resource.__import__ = Importer().new_import