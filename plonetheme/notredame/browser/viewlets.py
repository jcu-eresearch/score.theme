from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class PathBarViewlet(common.PathBarViewlet):
    """Customized breadcrumbs class
    """
    
    render = ViewPageTemplateFile('templates/pathbar.pt')