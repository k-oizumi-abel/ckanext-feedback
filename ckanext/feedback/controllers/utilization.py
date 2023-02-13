import ckan.plugins.toolkit as tk


class UtilizationController():

    # Render HTML pages
    # utilization/details.html
    def details():
        return tk.render("utilization/details.html")

    # utilization/registration.html
    def registration():
        return tk.render("utilization/registration.html")

    # utilization/comment_approval.html
    def comment_approval():
        return tk.render("utilization/comment_approval.html")

    # utilization/recommentview.html
    def comment():
        return tk.render("utilization/comment.html")

    # utilization/search.html
    def search():
        return tk.render("utilization/search.html")
