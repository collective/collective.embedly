import urllib2
import re
from urlparse import urlparse, parse_qsl
from collective.embedly.transform import get_services_regexp


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

        if self.url == 'http://api.embed.ly/1/services/python':
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

        if key is not None and len(key) != 32:
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
