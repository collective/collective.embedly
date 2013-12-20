import transaction
from plone.testing import z2
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
from Products.CMFCore.utils import getToolByName

from collective.embedly.tests.patch import patch_urlopen, unpatch_urlopen


def create_users(portal):
    acl_users = getToolByName(portal, 'acl_users')
    acl_users.userFolderAddUser('test_manager', 'secret', ['Manager'], [])
    acl_users.portal_role_manager.assignRolesToPrincipal(['Manager'],
                                                         'test_manager')


class Embedly(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.embedly
        xmlconfig.file('configure.zcml', collective.embedly,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.embedly:default')


class EmbedlyURLPatched(Embedly):

    def setUp(self):
        super(EmbedlyURLPatched, self).setUp()
        patch_urlopen()

    def tearDown(self):
        super(EmbedlyURLPatched, self).tearDown()
        unpatch_urlopen()


class EmbedlyFunctional(FunctionalTesting):

    def testSetUp(self):
        super(EmbedlyFunctional, self).testSetUp()
        create_users(self['portal'])
        transaction.commit()


EMBEDLY_FIXTURE = Embedly()
EMBEDLY_URL_PATCHED_FIXTURE = EmbedlyURLPatched()

EMBEDLY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EMBEDLY_URL_PATCHED_FIXTURE,),
    name="Embedly:Integration")

EMBEDLY_FUNCTIONAL_TESTING = EmbedlyFunctional(
    bases=(EMBEDLY_FIXTURE,),
    name="Embedly:Functional")

EMBEDLY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(EMBEDLY_URL_PATCHED_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Embedly:Acceptance")
