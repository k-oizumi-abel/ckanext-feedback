import ckan.plugins.toolkit as tk

class DownloadController:
#    def datasets():
#        return tk.render("")
#
#    def dataset_details():
#        return tk.render("")
#
#    def resource_details():
#        return tk.render("")

    def test():
        return tk.render("download/download.html")

    def increase_resource_download_count(target_resource_id):
        increase_resource_download_count(target_resource_id)
        return tk.render("download/download.html")