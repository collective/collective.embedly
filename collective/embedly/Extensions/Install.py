from Products.CMFCore.utils import getToolByName


def install(self):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.embedly:default')
    return "Imported install profile."


def uninstall(self):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.embedly:uninstall')
    return "Imported uninstall profile."
