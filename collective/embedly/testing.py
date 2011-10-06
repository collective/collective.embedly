from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class Embedly(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.embedly
        print "Loading zcml configurations"
        xmlconfig.file('configure.zcml', collective.embedly, context=configurationContext)

    def setUpPloneSite(self, portal):
        print "Applying default profile"
        applyProfile(portal, 'collective.embedly:default')

EMBEDLY_FIXTURE = Embedly()
EMBEDLY_INTEGRATION_TESTING = IntegrationTesting(
        bases=(EMBEDLY_FIXTURE,),
        name="Embedly:Integration")

EMBEDLY_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(EMBEDLY_FIXTURE,),
        name="Embedly:Functional")
