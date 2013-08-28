from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
import collective.embedly.transform
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.embedly.interfaces import IEmbedlySettings
TRANSFORM = 'embedly_transform'
SAFE = 'text/x-html-safe'
TINYMCE = {
    'customplugins': 'embedly|/++resource++collective.embedly.plugin/editor_plugin.js',
    'customtoolbarbuttons': 'embedlylink',
}
TINYMCEDROP = TINYMCE.copy()
TINYMCEDROP.update({
    'styles': 'Embedly link|a|embedlylink',
})


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        """
        Prevents uninstall profile from showing up in the profile list
        when creating a Plone site.
        """
        return [u'collective.embedly:uninstall']


def setupTransforms(portal):

    # add transform
    transform_tool = getToolByName(portal, 'portal_transforms')
    if not hasattr(transform_tool, TRANSFORM):
        transform_tool.manage_addTransform(
            TRANSFORM, 'collective.embedly.transform')

    # set policies
    for MT in (SAFE,):
        policies = [required
                    for (mimetype, required) in transform_tool.listPolicies()
                    if mimetype == MT]
        if policies:
            transform_tool.manage_delPolicies([MT])
            required = list(policies.pop())
        else:
            required = []

        for transform in [TRANSFORM]:
            if transform not in required:
                required.append(transform)
        transform_tool.manage_addPolicy(MT, required)


def removeTransforms(portal):

    # remove transform
    transform_tool = getToolByName(portal, 'portal_transforms')
    if hasattr(transform_tool, TRANSFORM):
        transform_tool.unregisterTransform(TRANSFORM)

    # set policies
    for MT in (SAFE,):
        policies = [required
                    for (mimetype, required) in transform_tool.listPolicies()
                    if mimetype == MT]
        if policies:
            transform_tool.manage_delPolicies([MT])
            required = list(policies.pop())
        else:
            required = []

        for transform in [TRANSFORM]:
            if transform in required:
                required.remove(transform)
        transform_tool.manage_addPolicy(MT, required)


def setupTinyMCEsettings(portal):
    tool = getToolByName(portal, 'portal_tinymce', None)
    if tool is None:
        return
    for key, value in TINYMCE.items():
        tool_value = getattr(tool, key)
        items = tool_value and tool_value.split('\n') or []
        if value not in items:
            items.append(value)
            tool_value = '\n'.join(items)
            setattr(tool, key, tool_value.decode())


def removeTinyMCEsettings(portal):
    tool = getToolByName(portal, 'portal_tinymce', None)
    if tool is None:
        return

    for key, value in TINYMCEDROP.items():
        tool_value = getattr(tool, key)
        items = tool_value and tool_value.split('\n') or []
        if value in items:
            items.remove(value)
            tool_value = '\n'.join(items)
            setattr(tool, key, tool_value.decode())


def importVarious(context):
    if context.readDataFile('collective.embedly.install.txt') is None:
        return
    portal = context.getSite()
    setupTransforms(portal)
    setupTinyMCEsettings(portal)


def removeVarious(context):
    if context.readDataFile('collective.embedly.uninstall.txt') is None:
        return
    portal = context.getSite()
    removeTransforms(portal)
    removeTinyMCEsettings(portal)


def add_tinymce_plugin(context):
    """Method to add TinyMCE plugin.
    """
    removeTinyMCEsettings(context)
    setupTinyMCEsettings(context)


def update_registry(context):
    """Method to update fields in registry.
    """
    registry = getUtility(IRegistry)
    registry.registerInterface(IEmbedlySettings)
