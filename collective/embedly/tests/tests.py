import urllib2
import json
import robotsuite
import unittest2 as unittest

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from plone.testing import layered

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login

from zope.annotation.interfaces import IAnnotations

from collective.embedly.interfaces import IEmbedlySettings
from collective.embedly.transform import get_oembed, parse
from collective.embedly.transform import match, update_services
from collective.embedly.tests.layer import EMBEDLY_INTEGRATION_TESTING
from collective.embedly.tests.layer import EMBEDLY_ACCEPTANCE_TESTING
from collective.embedly.tests.patch import json_result


class TestSetup(unittest.TestCase):
    layer = EMBEDLY_INTEGRATION_TESTING
    obj_url = "http://www.youtube.com/watch?v=L1NPLlhFTVk"

    def test_store_services(self):
        """ Test saving embedly services to site annotation """
        portal = self.layer['portal']
        storage = IAnnotations(portal)
        self.assertEqual(storage.get('collective.embedly.services'), None)
        update_services()

        res = urllib2.urlopen('http://api.embed.ly/1/services/python')
        list_exp = []
        for service in json.loads(res.read()):
            list_exp.append('|'.join(service.get('regex', [])))
        self.assertEqual(storage.get('collective.embedly.services'), '|'.join(list_exp))

    def test_embedly_params(self):
        """ Test query with additional embedly parameters """
        url = "http://www.youtube.com/watch?v=L1NPLlhFTVk&maxwidth=10&maxheight=10"
        res = get_oembed(url, None)
        self.assertEqual(res, json_result)

    def test_match_normal_url(self):
        """ Test matching valid link """
        self.assertTrue(match(self.obj_url))

    def test_match_not_valid_url(self):
        """ Test matching not valid link """
        self.assertFalse(match('http://not.valid.url/'))

    def test_replace_not_valid_url(self):
        """ Test replace not valid link """
        res = parse('<a class="external-link embedlylink" href="http://not.valid.url/11"></a>')
        self.assertFalse(res.startswith('<div class="embed">'))

    def test_image(self):
        """ Test image link transformation """
        res = parse('<a class="external-link embedlylink" href="http://www.flickr.com/photos/123.jpg"></a>')
        self.assertTrue(res.startswith('<div class="embed">'))

    def test_no_key_url(self):
        """ Test query with initial api_key """
        registry = getUtility(IRegistry)
        embedly_settings = registry.forInterface(IEmbedlySettings)
        self.assertFalse(embedly_settings.api_key)

        res = get_oembed(self.obj_url, embedly_settings.api_key)
        self.assertEqual(res, json_result)

    def test_normal_key(self):
        """ Test query with embedly api_key """
        res = get_oembed(self.obj_url, u'1234567890abcdef1234567890abcdef')
        self.assertEqual(res, json_result)

    def test_fake_key(self):
        """ Test query with not valid api_key """
        res = get_oembed(self.obj_url, u'1234')
        self.assertNotEqual(res, json_result)

    def test_empty_key(self):
        """ Test query with empty api_key """
        res = get_oembed(self.obj_url, u' ')
        self.assertEqual(res, json_result)

    def test_embedlylink_transformation(self):
        """ Test embedly link transformation """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Document', id='doc')
        portal.doc.setText('<a class="external-link embedlylink" href="%s"></a>' % self.obj_url)

        res = parse(portal.doc.getRawText())
        self.assertTrue(res.startswith('<div class="embed">'))

    def test_not_embedlylink_transformation(self):
        """ Test not embedly link transformation """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Document', id='doc')
        portal.doc.setText('<a class="external-link" href="%s"></a>' % self.obj_url)

        res = parse(portal.doc.getRawText())

        self.assertFalse(res.startswith('<div class="embed">'))

    def test_transform(self):
        """ Test url transformation """
        portal = self.layer['portal']
        pt = portal.portal_transforms
        data = '<a class="external-link embedlylink" href="%s"></a>' % self.obj_url
        res = pt.convertTo(target_mimetype='text/x-html-safe', orig=data, mimetype='text/html')
        res = res.getData()

        self.assertTrue(res.startswith('<div class="embed">'))

    def test_transform_real_document(self):
        """ Test url transformation in real document """
        portal = self.layer['portal']
        pt = portal.portal_transforms

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Document', id='doc')
        portal.doc.setText('<a class="external-link embedlylink" href="%s"></a>' % self.obj_url)
        data = portal.doc.getRawText()
        res = pt.convertTo(target_mimetype='text/x-html-safe', orig=data,
                           context=portal.doc, mimetype='text/html')
        res = res.getData()

        self.assertTrue(res.startswith('<div class="embed">'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_embedly.txt"),
                layer=EMBEDLY_ACCEPTANCE_TESTING),
    ])
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
