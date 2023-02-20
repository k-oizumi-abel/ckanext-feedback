import ckan.plugins.toolkit as toolkit


class UtilizationController:
    # Render HTML pages
    # utilization/details.html
    def details():
        return toolkit.render('utilization/details.html')

    # utilization/registration.html
    def registration():
        return toolkit.render('utilization/registration.html')

    # utilization/comment_approval.html
    def comment_approval():
        return toolkit.render('utilization/comment_approval.html')

    # utilization/recommentview.html
    def comment():
        return toolkit.render('utilization/comment.html')

    # utilization/search.html
    def search():
        return toolkit.render('utilization/search.html')
