from plone.testing import z2
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
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
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory(
            "Folder",
            id="acceptance-test-folder",
            title=u"Test Folder"
        )


EMBEDLY_FIXTURE = Embedly()
EMBEDLY_INTEGRATION_TESTING = IntegrationTesting(
        bases=(EMBEDLY_FIXTURE,),
        name="Embedly:Integration")

EMBEDLY_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(EMBEDLY_FIXTURE,),
        name="Embedly:Functional")

EMBEDLY_ACCEPTANCE_TESTING = FunctionalTesting(
        bases=(EMBEDLY_FIXTURE, z2.ZSERVER_FIXTURE),
        name="Embedly:Acceptance")
