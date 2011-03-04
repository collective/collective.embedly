from Products.CMFCore.utils import getToolByName
import collective.embedly.transform
TRANSFORM = 'embedly_transform'
SAFE = 'text/x-html-safe'
STYLE = 'Embedly link|a|embedlylink'

def setupTransforms(portal):

    # add transform
    transform_tool = getToolByName(portal, 'portal_transforms')
    if not hasattr(transform_tool, TRANSFORM):
        transform_tool.manage_addTransform(TRANSFORM, 'collective.embedly.transform')

    # set policies
    for MT in (SAFE,):
        policies = [required for (mimetype, required) in transform_tool.listPolicies()
            if mimetype==MT]
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
        policies = [required for (mimetype, required) in transform_tool.listPolicies()
            if mimetype==MT]
        if policies:
            transform_tool.manage_delPolicies([MT])
            required = list(policies.pop())
        else:
            required = []

        for transform in [TRANSFORM]:
            if transform in required:
                required.remove(transform)
        transform_tool.manage_addPolicy(MT, required)

def setupTMCEstyles(portal):
    tool = getToolByName(portal, 'portal_tinymce', None)
    if tool is None:
        return
    styles = getattr(tool, 'styles')
    items = styles.split('\n')
    if STYLE not in items: 
        items.append(STYLE)
        styles = '\n'.join(items)
        setattr(tool, 'styles', styles)

def removeTMCEstyles(portal):
    tool = getToolByName(portal, 'portal_tinymce', None)
    if tool is None:
        return
    styles = getattr(tool, 'styles')
    items = styles.split('\n')
    if STYLE in items: 
        items.remove(STYLE)
        styles = '\n'.join(items)
        setattr(tool, 'styles', styles)

def importVarious(context):
    if context.readDataFile('collective.embedly.install.txt') is None:
        return
    portal = context.getSite()
    setupTransforms(portal)
    setupTMCEstyles(portal)

def removeVarious(context):
    if context.readDataFile('collective.embedly.uninstall.txt') is None:
        return
    portal = context.getSite()
    removeTransforms(portal)
    removeTMCEstyles(portal)
