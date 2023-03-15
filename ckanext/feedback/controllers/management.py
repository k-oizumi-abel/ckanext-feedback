from ckan.plugins import toolkit


class ManagementController:
    # management/comments.html
    @staticmethod
    def comments():
        return toolkit.render('management/comments.html')
