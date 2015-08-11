from Products.Five.browser import BrowserView
from collective.embedly.transform import get_embedly_settings


class EmbedlyPlugin(BrowserView):

    def api_key(self):
        return get_embedly_settings('api_key')
