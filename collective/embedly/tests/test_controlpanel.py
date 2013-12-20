import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from collective.embedly.interfaces import IEmbedlySettings
from collective.embedly.tests.layer import EMBEDLY_FUNCTIONAL_TESTING


class TestControlPanel(unittest.TestCase):
    """
    Test collective.embedly control panel
    """
    layer = EMBEDLY_FUNCTIONAL_TESTING

    def setUp(self):
        """
        Configure browser and log in to the portal as manager
        """
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.open("%s/login_form" % self.portal_url)
        self.browser.getControl(name='__ac_name').value = 'test_manager'
        self.browser.getControl(name='__ac_password').value = 'secret'
        self.browser.getControl(name='submit').click()
        self.browser.getLink('Continue to the Plone site home page').click()

    def testControlPanel(self):
        """
        Test control panel access
        """
        browser = self.browser
        browser.open('http://nohost/plone/plone_control_panel')
        self.failUnless('Embedly' in self.browser.contents)

    def testCancel(self):
        """
        Test cancel button
        """
        browser = self.browser
        browser.open('http://nohost/plone/@@embedly-controlpanel')
        self.assertEquals(browser.url, 'http://nohost/plone/@@embedly-controlpanel')
        self.browser.getControl(name="form.actions.cancel").click()
        self.failUnless(self.browser.url.endswith('plone_control_panel'))
        self.failUnless('Changes canceled.' in self.browser.contents)

    def testOptions(self):
        """
        Test changing values
        """
        browser = self.browser
        browser.open('http://nohost/plone/@@embedly-controlpanel')

        self.assertEquals(browser.getControl(name='form.api_key').value, '')
        self.assertEquals(browser.getControl(name='form.use_services_regexp').value, True)
        self.assertEquals(browser.getControl(name='form.persistent_cache').value, False)
        self.assertEquals(browser.getControl(name='form.cache_timeout').value, '86400')

        browser.getControl(name='form.api_key').value = u'MY_KEY'
        browser.getControl(name='form.use_services_regexp').value = False
        browser.getControl(name='form.persistent_cache').value = True
        browser.getControl(name='form.cache_timeout').value = '1000'
        self.browser.getControl(name="form.actions.save").click()
        self.failUnless('Changes saved.' in self.browser.contents)

        registry = getUtility(IRegistry).forInterface(IEmbedlySettings)
        self.assertEquals(registry.api_key, 'MY_KEY')
        self.assertEquals(registry.use_services_regexp, False)
        self.assertEquals(registry.persistent_cache, True)
        self.assertEquals(registry.cache_timeout, 1000)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestControlPanel))
    return suite
