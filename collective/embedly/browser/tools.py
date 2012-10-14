from Products.Five.browser import BrowserView
from collective.embedly.transform import update_services


class UpdateServicesView(BrowserView):
    def __call__(self):
        if update_services():
            return "Services list updated."
        else:
            return "Problems with connection to embed.ly. Check internet connection."
