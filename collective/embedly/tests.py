import urllib2
import urllib
import re
import json
import logging
import unittest2 as unittest
from urlparse import urlparse, parse_qsl

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login

from zope.annotation.interfaces import IAnnotations

from collective.embedly.testing import EMBEDLY_INTEGRATION_TESTING
from collective.embedly.interfaces import IEmbedlySettings
from collective.embedly.transform import get_oembed, parse, get_services_regexp
from collective.embedly.transform import match, update_services, replace

from Products.CMFCore.utils import getToolByName


embedly_data = '{"provider_url": "http://www.youtube.com/", "description": "HAYDAMAKY message", "title": "HAYDAMAKY message", "url": "http://www.youtube.com/watch?v=L1NPLlhFTVk", "author_name": "eastblok", "height": 360, "width": 640, "html": "<object width=\\"640\\" height=\\"360\\"><param name=\\"movie\\" value=\\"http://www.youtube.com/v/L1NPLlhFTVk?version=3\\"><param name=\\"allowFullScreen\\" value=\\"true\\"><param name=\\"allowscriptaccess\\" value=\\"always\\"><embed src=\\"http://www.youtube.com/v/L1NPLlhFTVk?version=3\\" type=\\"application/x-shockwave-flash\\" width=\\"640\\" height=\\"360\\" allowscriptaccess=\\"always\\" allowfullscreen=\\"true\\"></embed></object>", "thumbnail_width": 480, "version": "1.0", "provider_name": "YouTube", "thumbnail_url": "http://i1.ytimg.com/vi/L1NPLlhFTVk/hqdefault.jpg", "type": "video", "thumbnail_height": 360, "author_url": "http://www.youtube.com/user/eastblok"}'

embedly_photo_data = '{"provider_url": "http://www.flickr.com/", "description": "Description.", "title": "Title", "url": "http://www.flickr.com/123.jpg", "author_name": "Test", "height": 200, "width": 400, "thumbnail_url": "http://www.flickr.com/123_thumb.jpg", "thumbnail_width": 100, "version": "1.0", "provider_name": "Flickr", "cache_age": 3600, "type": "photo", "thumbnail_height": 75, "author_url": "http://www.flickr.com/photos/test"}'

json_result = {u'provider_url': u'http://www.youtube.com/', u'description': u'HAYDAMAKY message', u'title': u'HAYDAMAKY message', u'url': u'http://www.youtube.com/watch?v=L1NPLlhFTVk', u'type': u'video', u'author_name': u'eastblok', u'height': 360, u'width': 640, u'html': u'<object width="640" height="360"><param name="movie" value="http://www.youtube.com/v/L1NPLlhFTVk?version=3"><param name="allowFullScreen" value="true"><param name="allowscriptaccess" value="always"><embed src="http://www.youtube.com/v/L1NPLlhFTVk?version=3" type="application/x-shockwave-flash" width="640" height="360" allowscriptaccess="always" allowfullscreen="true"></embed></object>', u'thumbnail_width': 480, u'version': u'1.0', u'provider_name': u'YouTube', u'thumbnail_url': u'http://i1.ytimg.com/vi/L1NPLlhFTVk/hqdefault.jpg', u'thumbnail_height': 360, u'author_url': u'http://www.youtube.com/user/eastblok'}

dummy_services = '[{"regex": ["http://.*youtube\\\\.com/watch.*", "http://.*\\\\.youtube\\\\.com/v/.*", "https://.*youtube\\\\.com/watch.*", "https://.*\\\\.youtube\\\\.com/v/.*", "http://youtu\\\\.be/.*", "http://.*\\\\.youtube\\\\.com/user/.*", "http://.*\\\\.youtube\\\\.com/.*\\\\#.*/.*", "http://m\\\\.youtube\\\\.com/watch.*", "http://m\\\\.youtube\\\\.com/index.*", "http://.*\\\\.youtube\\\\.com/profile.*", "http://.*\\\\.youtube\\\\.com/view_play_list.*", "http://.*\\\\.youtube\\\\.com/playlist.*"], "about": "About", "displayname": "YouTube", "name": "youtube", "domain": "youtube.com", "subdomains": ["m.youtube.com"], "favicon": "http://c2548752.cdn.cloudfiles.rackspacecloud.com/youtube.ico", "type": "video"}, {"regex": ["http://.*justin\\\\.tv/.*", "http://.*justin\\\\.tv/.*/w/.*"], "about": "About", "displayname": "Justin.tv", "name": "justintv", "domain": "justin.tv", "subdomains": [], "favicon": "http://c2548752.cdn.cloudfiles.rackspacecloud.com/justintv.ico", "type": "video"}, {"regex": ["http://www\\\\.flickr\\\\.com/photos/.*", "http://flic\\\\.kr/.*"], "about": "About", "displayname": "Flickr", "name": "flickr", "domain": "flickr.com", "subdomains": [], "favicon": "http://c2548752.cdn.cloudfiles.rackspacecloud.com/flickr.ico", "type": "photo"}]'

class dummy_urlopen():
    code = 200

    def __init__(self, url, **kw):
        self.url = url

    def getcode(self):
        return self.code

    def read(self):

        if self.url == 'http://api.embed.ly/v1/api/services/python':
            # embedly services query
            return dummy_services

        parts = urlparse(self.url)
        params = parse_qsl(parts.query)

        key = None
        for p in params:
            if p[0] == 'key':
                key = p[1]
            if p[0] == 'url':
                service_url = p[1]

        if key is not None and len(key)!=32:
            from StringIO import StringIO
            raise urllib2.HTTPError(self.url, 401, 'Unauthorized', None,
                                    StringIO('Invalid key or oauth_consumer_key provided: %s' % key))
        if re.match(get_services_regexp(), service_url):
            if service_url.endswith('.jpg'):
                return embedly_photo_data
            else:
                return embedly_data
        else:
            return None

    def close(self):
        pass

original_urlopen = urllib2.urlopen

def patch_urlopen():
    global original_urlopen
    original_urlopen = urllib2.urlopen
    urllib2.urlopen = dummy_urlopen


def unpatch_urlopen():
    urllib2.urlopen = original_urlopen


class TestSetup(unittest.TestCase):
    layer = EMBEDLY_INTEGRATION_TESTING
    obj_url = "http://www.youtube.com/watch?v=L1NPLlhFTVk"

    def setUp(self):
        patch_urlopen()

    def tearDown(self):
        unpatch_urlopen()

    def test_store_services(self):
        """ Test saving embedly services to site annotation """
        portal = self.layer['portal']
        storage = IAnnotations(portal)
        self.assertEqual(storage.get('collective.embedly.services'), None)
        update_services()

        res = urllib2.urlopen('http://api.embed.ly/v1/api/services/python')
        list_exp = []
        for service in json.loads(res.read()):
            list_exp.append('|'.join(service.get('regex',[])))
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
        doc = portal.invokeFactory('Document', id='doc')
        portal.doc.setText('<a class="external-link embedlylink" href="%s"></a>' % self.obj_url)

        res = parse(portal.doc.getRawText())
        self.assertTrue(res.startswith('<div class="embed">'))

    def test_not_embedlylink_transformation(self):
        """ Test not embedly link transformation """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        doc = portal.invokeFactory('Document', id='doc')
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
        doc = portal.invokeFactory('Document', id='doc')
        portal.doc.setText('<a class="external-link embedlylink" href="%s"></a>' % self.obj_url)
        data = portal.doc.getRawText()
        res = pt.convertTo(target_mimetype='text/x-html-safe', orig=data,
                           context=portal.doc, mimetype='text/html')
        res = res.getData()

        self.assertTrue(res.startswith('<div class="embed">'))
