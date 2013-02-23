from plone.testing import z2
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
from collective.embedly.tests.patch import patch_urlopen, unpatch_urlopen


class Embedly(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.embedly
        xmlconfig.file('configure.zcml', collective.embedly, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.embedly:default')

    def setUp(self):
        super(Embedly, self).setUp()
        patch_urlopen()

    def tearDown(self):
        super(Embedly, self).tearDown()
        unpatch_urlopen()

EMBEDLY_FIXTURE = Embedly()
EMBEDLY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EMBEDLY_FIXTURE,),
    name="Embedly:Integration")

EMBEDLY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(EMBEDLY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Embedly:Acceptance")
