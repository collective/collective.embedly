from Products.CMFCore.utils import getToolByName
import collective.embedly.transform


def setupTransforms(context):

    portal = context.getSite()
    TRANSFORM = 'embedly_transform'
    SAFE = 'text/x-html-safe'

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


def importVarious(context):
    if context.readDataFile('marker.txt') is None:
        return
    portal = context.getSite()
    setupTransforms(context)

