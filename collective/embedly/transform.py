import urllib2
import urllib
import json
import re
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements
from plone.memoize import ram
from time import time

link_url_re = re.compile('(?P<link><a.*?embedlylink.*? href=[\'"]?(?P<url>[^\'"# >]+).*?</a>)')
embedly_re = re.compile("http://(.*youtube\.com/watch.*|.*\.youtube\.com/v/.*|youtu\.be/.*|.*\.youtube\.com/user/.*|.*\.youtube\.com/.*#.*/.*|m\.youtube\.com/watch.*|m\.youtube\.com/index.*|.*\.youtube\.com/profile.*|.*justin\.tv/.*|.*justin\.tv/.*/b/.*|.*justin\.tv/.*/w/.*|www\.ustream\.tv/recorded/.*|www\.ustream\.tv/channel/.*|www\.ustream\.tv/.*|qik\.com/video/.*|qik\.com/.*|qik\.ly/.*|.*revision3\.com/.*|.*\.dailymotion\.com/video/.*|.*\.dailymotion\.com/.*/video/.*|www\.collegehumor\.com/video:.*|.*twitvid\.com/.*|www\.break\.com/.*/.*|vids\.myspace\.com/index\.cfm\?fuseaction=vids\.individual&videoid.*|www\.myspace\.com/index\.cfm\?fuseaction=.*&videoid.*|www\.metacafe\.com/watch/.*|www\.metacafe\.com/w/.*|blip\.tv/file/.*|.*\.blip\.tv/file/.*|video\.google\.com/videoplay\?.*|.*revver\.com/video/.*|video\.yahoo\.com/watch/.*/.*|video\.yahoo\.com/network/.*|.*viddler\.com/explore/.*/videos/.*|liveleak\.com/view\?.*|www\.liveleak\.com/view\?.*|animoto\.com/play/.*|dotsub\.com/view/.*|www\.overstream\.net/view\.php\?oid=.*|www\.livestream\.com/.*|www\.worldstarhiphop\.com/videos/video.*\.php\?v=.*|worldstarhiphop\.com/videos/video.*\.php\?v=.*|teachertube\.com/viewVideo\.php.*|www\.teachertube\.com/viewVideo\.php.*|www1\.teachertube\.com/viewVideo\.php.*|www2\.teachertube\.com/viewVideo\.php.*|bambuser\.com/v/.*|bambuser\.com/channel/.*|bambuser\.com/channel/.*/broadcast/.*|www\.schooltube\.com/video/.*/.*|bigthink\.com/ideas/.*|bigthink\.com/series/.*|sendables\.jibjab\.com/view/.*|sendables\.jibjab\.com/originals/.*|www\.xtranormal\.com/watch/.*|dipdive\.com/media/.*|dipdive\.com/member/.*/media/.*|dipdive\.com/v/.*|.*\.dipdive\.com/media/.*|.*\.dipdive\.com/v/.*|v\.youku\.com/v_show/.*\.html|v\.youku\.com/v_playlist/.*\.html|www\.snotr\.com/video/.*|snotr\.com/video/.*|.*yfrog\..*/.*|tweetphoto\.com/.*|www\.flickr\.com/photos/.*|flic\.kr/.*|twitpic\.com/.*|www\.twitpic\.com/.*|twitpic\.com/photos/.*|www\.twitpic\.com/photos/.*|.*imgur\.com/.*|.*\.posterous\.com/.*|post\.ly/.*|twitgoo\.com/.*|i.*\.photobucket\.com/albums/.*|s.*\.photobucket\.com/albums/.*|phodroid\.com/.*/.*/.*|www\.mobypicture\.com/user/.*/view/.*|moby\.to/.*|xkcd\.com/.*|www\.xkcd\.com/.*|imgs\.xkcd\.com/.*|www\.asofterworld\.com/index\.php\?id=.*|www\.asofterworld\.com/.*\.jpg|asofterworld\.com/.*\.jpg|www\.qwantz\.com/index\.php\?comic=.*|23hq\.com/.*/photo/.*|www\.23hq\.com/.*/photo/.*|.*dribbble\.com/shots/.*|drbl\.in/.*|.*\.smugmug\.com/.*|.*\.smugmug\.com/.*#.*|emberapp\.com/.*/images/.*|emberapp\.com/.*/images/.*/sizes/.*|emberapp\.com/.*/collections/.*/.*|emberapp\.com/.*/categories/.*/.*/.*|embr\.it/.*|picasaweb\.google\.com.*/.*/.*#.*|picasaweb\.google\.com.*/lh/photo/.*|picasaweb\.google\.com.*/.*/.*|dailybooth\.com/.*/.*|brizzly\.com/pic/.*|pics\.brizzly\.com/.*\.jpg|img\.ly/.*|www\.tinypic\.com/view\.php.*|tinypic\.com/view\.php.*|www\.tinypic\.com/player\.php.*|tinypic\.com/player\.php.*|www\.tinypic\.com/r/.*/.*|tinypic\.com/r/.*/.*|.*\.tinypic\.com/.*\.jpg|.*\.tinypic\.com/.*\.png|meadd\.com/.*/.*|meadd\.com/.*|.*\.deviantart\.com/art/.*|.*\.deviantart\.com/gallery/.*|.*\.deviantart\.com/#/.*|fav\.me/.*|.*\.deviantart\.com|.*\.deviantart\.com/gallery|.*\.deviantart\.com/.*/.*\.jpg|.*\.deviantart\.com/.*/.*\.gif|.*\.deviantart\.net/.*/.*\.jpg|.*\.deviantart\.net/.*/.*\.gif|plixi\.com/p/.*|plixi\.com/profile/home/.*|plixi\.com/.*|www\.fotopedia\.com/.*/.*|fotopedia\.com/.*/.*|photozou\.jp/photo/show/.*/.*|photozou\.jp/photo/photo_only/.*/.*|instagr\.am/p/.*|skitch\.com/.*/.*/.*|img\.skitch\.com/.*|https://skitch\.com/.*/.*/.*|https://img\.skitch\.com/.*|share\.ovi\.com/media/.*/.*|www\.questionablecontent\.net/|questionablecontent\.net/|www\.questionablecontent\.net/view\.php.*|questionablecontent\.net/view\.php.*|questionablecontent\.net/comics/.*\.png|www\.questionablecontent\.net/comics/.*\.png|picplz\.com/user/.*/pic/.*/|twitrpix\.com/.*|.*\.twitrpix\.com/.*|www\.someecards\.com/.*/.*|someecards\.com/.*/.*|some\.ly/.*|www\.some\.ly/.*|pikchur\.com/.*|achewood\.com/.*|www\.achewood\.com/.*|achewood\.com/index\.php.*|www\.achewood\.com/index\.php.*|www\.whitehouse\.gov/photos-and-video/video/.*|www\.whitehouse\.gov/video/.*|wh\.gov/photos-and-video/video/.*|wh\.gov/video/.*|www\.hulu\.com/watch.*|www\.hulu\.com/w/.*|hulu\.com/watch.*|hulu\.com/w/.*|.*crackle\.com/c/.*|www\.fancast\.com/.*/videos|www\.funnyordie\.com/videos/.*|www\.funnyordie\.com/m/.*|funnyordie\.com/videos/.*|funnyordie\.com/m/.*|www\.vimeo\.com/groups/.*/videos/.*|www\.vimeo\.com/.*|vimeo\.com/groups/.*/videos/.*|vimeo\.com/.*|vimeo\.com/m/#/.*|www\.ted\.com/talks/.*\.html.*|www\.ted\.com/talks/lang/.*/.*\.html.*|www\.ted\.com/index\.php/talks/.*\.html.*|www\.ted\.com/index\.php/talks/lang/.*/.*\.html.*|.*nfb\.ca/film/.*|www\.thedailyshow\.com/watch/.*|www\.thedailyshow\.com/full-episodes/.*|www\.thedailyshow\.com/collection/.*/.*/.*|movies\.yahoo\.com/movie/.*/video/.*|movies\.yahoo\.com/movie/.*/trailer|movies\.yahoo\.com/movie/.*/video|www\.colbertnation\.com/the-colbert-report-collections/.*|www\.colbertnation\.com/full-episodes/.*|www\.colbertnation\.com/the-colbert-report-videos/.*|www\.comedycentral\.com/videos/index\.jhtml\?.*|www\.theonion\.com/video/.*|theonion\.com/video/.*|wordpress\.tv/.*/.*/.*/.*/|www\.traileraddict\.com/trailer/.*|www\.traileraddict\.com/clip/.*|www\.traileraddict\.com/poster/.*|www\.escapistmagazine\.com/videos/.*|www\.trailerspy\.com/trailer/.*/.*|www\.trailerspy\.com/trailer/.*|www\.trailerspy\.com/view_video\.php.*|www\.atom\.com/.*/.*/|fora\.tv/.*/.*/.*/.*|www\.spike\.com/video/.*|www\.gametrailers\.com/video/.*|gametrailers\.com/video/.*|www\.koldcast\.tv/video/.*|www\.koldcast\.tv/#video:.*|techcrunch\.tv/watch.*|techcrunch\.tv/.*/watch.*|mixergy\.com/.*|video\.pbs\.org/video/.*|www\.zapiks\.com/.*|tv\.digg\.com/diggnation/.*|tv\.digg\.com/diggreel/.*|tv\.digg\.com/diggdialogg/.*|www\.trutv\.com/video/.*|www\.nzonscreen\.com/title/.*|nzonscreen\.com/title/.*|app\.wistia\.com/embed/medias/.*|https://app\.wistia\.com/embed/medias/.*|hungrynation\.tv/.*/episode/.*|www\.hungrynation\.tv/.*/episode/.*|hungrynation\.tv/episode/.*|www\.hungrynation\.tv/episode/.*|indymogul\.com/.*/episode/.*|www\.indymogul\.com/.*/episode/.*|indymogul\.com/episode/.*|www\.indymogul\.com/episode/.*|channelfrederator\.com/.*/episode/.*|www\.channelfrederator\.com/.*/episode/.*|channelfrederator\.com/episode/.*|www\.channelfrederator\.com/episode/.*|tmiweekly\.com/.*/episode/.*|www\.tmiweekly\.com/.*/episode/.*|tmiweekly\.com/episode/.*|www\.tmiweekly\.com/episode/.*|99dollarmusicvideos\.com/.*/episode/.*|www\.99dollarmusicvideos\.com/.*/episode/.*|99dollarmusicvideos\.com/episode/.*|www\.99dollarmusicvideos\.com/episode/.*|ultrakawaii\.com/.*/episode/.*|www\.ultrakawaii\.com/.*/episode/.*|ultrakawaii\.com/episode/.*|www\.ultrakawaii\.com/episode/.*|barelypolitical\.com/.*/episode/.*|www\.barelypolitical\.com/.*/episode/.*|barelypolitical\.com/episode/.*|www\.barelypolitical\.com/episode/.*|barelydigital\.com/.*/episode/.*|www\.barelydigital\.com/.*/episode/.*|barelydigital\.com/episode/.*|www\.barelydigital\.com/episode/.*|threadbanger\.com/.*/episode/.*|www\.threadbanger\.com/.*/episode/.*|threadbanger\.com/episode/.*|www\.threadbanger\.com/episode/.*|vodcars\.com/.*/episode/.*|www\.vodcars\.com/.*/episode/.*|vodcars\.com/episode/.*|www\.vodcars\.com/episode/.*|confreaks\.net/videos/.*|www\.confreaks\.net/videos/.*|video\.allthingsd\.com/video/.*|aniboom\.com/animation-video/.*|www\.aniboom\.com/animation-video/.*|clipshack\.com/Clip\.aspx\?.*|www\.clipshack\.com/Clip\.aspx\?.*|grindtv\.com/.*/video/.*|www\.grindtv\.com/.*/video/.*|ifood\.tv/recipe/.*|ifood\.tv/video/.*|ifood\.tv/channel/user/.*|www\.ifood\.tv/recipe/.*|www\.ifood\.tv/video/.*|www\.ifood\.tv/channel/user/.*|logotv\.com/video/.*|www\.logotv\.com/video/.*|lonelyplanet\.com/Clip\.aspx\?.*|www\.lonelyplanet\.com/Clip\.aspx\?.*|streetfire\.net/video/.*\.htm.*|www\.streetfire\.net/video/.*\.htm.*|trooptube\.tv/videos/.*|www\.trooptube\.tv/videos/.*|www\.godtube\.com/featured/video/.*|godtube\.com/featured/video/.*|www\.godtube\.com/watch/.*|godtube\.com/watch/.*|www\.tangle\.com/view_video.*|mediamatters\.org/mmtv/.*|www\.clikthrough\.com/theater/video/.*|soundcloud\.com/.*|soundcloud\.com/.*/.*|soundcloud\.com/.*/sets/.*|soundcloud\.com/groups/.*|snd\.sc/.*|www\.last\.fm/music/.*|www\.last\.fm/music/+videos/.*|www\.last\.fm/music/+images/.*|www\.last\.fm/music/.*/_/.*|www\.last\.fm/music/.*/.*|www\.mixcloud\.com/.*/.*/|www\.radionomy\.com/.*/radio/.*|radionomy\.com/.*/radio/.*|www\.entertonement\.com/clips/.*|www\.rdio\.com/#/artist/.*/album/.*|www\.rdio\.com/artist/.*/album/.*|www\.zero-inch\.com/.*|.*\.bandcamp\.com/|.*\.bandcamp\.com/track/.*|.*\.bandcamp\.com/album/.*|freemusicarchive\.org/music/.*|www\.freemusicarchive\.org/music/.*|freemusicarchive\.org/curator/.*|www\.freemusicarchive\.org/curator/.*|www\.npr\.org/.*/.*/.*/.*/.*|www\.npr\.org/.*/.*/.*/.*/.*/.*|www\.npr\.org/.*/.*/.*/.*/.*/.*/.*|www\.npr\.org/templates/story/story\.php.*|huffduffer\.com/.*/.*|www\.audioboo\.fm/boos/.*|audioboo\.fm/boos/.*|boo\.fm/b.*|www\.xiami\.com/song/.*|xiami\.com/song/.*|www\.saynow\.com/playMsg\.html.*|www\.saynow\.com/playMsg\.html.*|listen\.grooveshark\.com/s/.*|espn\.go\.com/video/clip.*|espn\.go\.com/.*/story.*|abcnews\.com/.*/video/.*|abcnews\.com/video/playerIndex.*|washingtonpost\.com/wp-dyn/.*/video/.*/.*/.*/.*|www\.washingtonpost\.com/wp-dyn/.*/video/.*/.*/.*/.*|www\.boston\.com/video.*|boston\.com/video.*|www\.facebook\.com/photo\.php.*|www\.facebook\.com/video/video\.php.*|www\.facebook\.com/v/.*|cnbc\.com/id/.*\?.*video.*|www\.cnbc\.com/id/.*\?.*video.*|cnbc\.com/id/.*/play/1/video/.*|www\.cnbc\.com/id/.*/play/1/video/.*|cbsnews\.com/video/watch/.*|www\.google\.com/buzz/.*/.*/.*|www\.google\.com/buzz/.*|www\.google\.com/profiles/.*|google\.com/buzz/.*/.*/.*|google\.com/buzz/.*|google\.com/profiles/.*|www\.cnn\.com/video/.*|edition\.cnn\.com/video/.*|money\.cnn\.com/video/.*|today\.msnbc\.msn\.com/id/.*/vp/.*|www\.msnbc\.msn\.com/id/.*/vp/.*|www\.msnbc\.msn\.com/id/.*/ns/.*|today\.msnbc\.msn\.com/id/.*/ns/.*|multimedia\.foxsports\.com/m/video/.*/.*|msn\.foxsports\.com/video.*|www\.globalpost\.com/video/.*|www\.globalpost\.com/dispatch/.*|guardian\.co\.uk/.*/video/.*/.*/.*/.*|www\.guardian\.co\.uk/.*/video/.*/.*/.*/.*|bravotv\.com/.*/.*/videos/.*|www\.bravotv\.com/.*/.*/videos/.*|video\.nationalgeographic\.com/.*/.*/.*\.html|dsc\.discovery\.com/videos/.*|animal\.discovery\.com/videos/.*|health\.discovery\.com/videos/.*|investigation\.discovery\.com/videos/.*|military\.discovery\.com/videos/.*|planetgreen\.discovery\.com/videos/.*|science\.discovery\.com/videos/.*|tlc\.discovery\.com/videos/.*|.*amazon\..*/gp/product/.*|.*amazon\..*/.*/dp/.*|.*amazon\..*/dp/.*|.*amazon\..*/o/ASIN/.*|.*amazon\..*/gp/offer-listing/.*|.*amazon\..*/.*/ASIN/.*|.*amazon\..*/gp/product/images/.*|www\.amzn\.com/.*|amzn\.com/.*|www\.shopstyle\.com/browse.*|www\.shopstyle\.com/action/apiVisitRetailer.*|api\.shopstyle\.com/action/apiVisitRetailer.*|www\.shopstyle\.com/action/viewLook.*|gist\.github\.com/.*|twitter\.com/.*/status/.*|twitter\.com/.*/statuses/.*|www\.twitter\.com/.*/status/.*|www\.twitter\.com/.*/statuses/.*|mobile\.twitter\.com/.*/status/.*|mobile\.twitter\.com/.*/statuses/.*|www\.crunchbase\.com/.*/.*|crunchbase\.com/.*/.*|www\.slideshare\.net/.*/.*|www\.slideshare\.net/mobile/.*/.*|slidesha\.re/.*|.*\.scribd\.com/doc/.*|screenr\.com/.*|polldaddy\.com/community/poll/.*|polldaddy\.com/poll/.*|answers\.polldaddy\.com/poll/.*|www\.5min\.com/Video/.*|www\.howcast\.com/videos/.*|www\.screencast\.com/.*/media/.*|screencast\.com/.*/media/.*|www\.screencast\.com/t/.*|screencast\.com/t/.*|issuu\.com/.*/docs/.*|www\.kickstarter\.com/projects/.*/.*|www\.scrapblog\.com/viewer/viewer\.aspx.*|ping\.fm/p/.*|chart\.ly/symbols/.*|chart\.ly/.*|maps\.google\.com/maps\?.*|maps\.google\.com/\?.*|maps\.google\.com/maps/ms\?.*|.*\.craigslist\.org/.*/.*|my\.opera\.com/.*/albums/show\.dml\?id=.*|my\.opera\.com/.*/albums/showpic\.dml\?album=.*&picture=.*|tumblr\.com/.*|.*\.tumblr\.com/post/.*|www\.polleverywhere\.com/polls/.*|www\.polleverywhere\.com/multiple_choice_polls/.*|www\.polleverywhere\.com/free_text_polls/.*|www\.quantcast\.com/wd:.*|www\.quantcast\.com/.*|siteanalytics\.compete\.com/.*|statsheet\.com/statplot/charts/.*/.*/.*/.*|statsheet\.com/statplot/charts/e/.*|statsheet\.com/.*/teams/.*/.*|statsheet\.com/tools/chartlets\?chart=.*|.*\.status\.net/notice/.*|identi\.ca/notice/.*|brainbird\.net/notice/.*|shitmydadsays\.com/notice/.*|www\.studivz\.net/Profile/.*|www\.studivz\.net/l/.*|www\.studivz\.net/Groups/Overview/.*|www\.studivz\.net/Gadgets/Info/.*|www\.studivz\.net/Gadgets/Install/.*|www\.studivz\.net/.*|www\.meinvz\.net/Profile/.*|www\.meinvz\.net/l/.*|www\.meinvz\.net/Groups/Overview/.*|www\.meinvz\.net/Gadgets/Info/.*|www\.meinvz\.net/Gadgets/Install/.*|www\.meinvz\.net/.*|www\.schuelervz\.net/Profile/.*|www\.schuelervz\.net/l/.*|www\.schuelervz\.net/Groups/Overview/.*|www\.schuelervz\.net/Gadgets/Info/.*|www\.schuelervz\.net/Gadgets/Install/.*|www\.schuelervz\.net/.*|myloc\.me/.*|pastebin\.com/.*|pastie\.org/.*|www\.pastie\.org/.*|redux\.com/stream/item/.*/.*|redux\.com/f/.*/.*|www\.redux\.com/stream/item/.*/.*|www\.redux\.com/f/.*/.*|cl\.ly/.*|cl\.ly/.*/content|speakerdeck\.com/u/.*/p/.*|www\.kiva\.org/lend/.*|www\.timetoast\.com/timelines/.*|storify\.com/.*/.*|.*meetup\.com/.*|meetu\.ps/.*|www\.dailymile\.com/people/.*/entries/.*|.*\.kinomap\.com/.*|www\.metacdn\.com/api/users/.*/content/.*|www\.metacdn\.com/api/users/.*/media/.*|prezi\.com/.*/.*|.*\.uservoice\.com/.*/suggestions/.*|formspring\.me/.*|www\.formspring\.me/.*|formspring\.me/.*/q/.*|www\.formspring\.me/.*/q/.*|twitlonger\.com/show/.*|www\.twitlonger\.com/show/.*|tl\.gd/.*|www\.qwiki\.com/q/.*)", re.I)
MAX_WIDTH = 600
get_services_from_embedly = False

@ram.cache(lambda *args: True)
def get_services():
    result = urllib2.urlopen('http://api.embed.ly/v1/api/services/python').read()
    return json.loads(result)

@ram.cache(lambda method, url: (time() // (60 * 60 * 24), url))
def get_oembed(url):
    params = {'url' : url,
              'maxwidth' : MAX_WIDTH,
              'format' : 'json'}
    fetch_url = 'http://api.embed.ly/v1/api/oembed?%s' % urllib.urlencode(params)
    try:
        result = urllib2.urlopen(fetch_url).read()
    except:
        return None
    return json.loads(result)

@ram.cache(lambda method, url: url)
def match(url):
    if get_services_from_embedly:
        for service in get_services():
            for regex in service['regex']:
                if re.match(regex, url):
                    return True
    else:
        if re.match(embedly_re, url):
            return True
    return False

def replace(matchobj):
    url = matchobj.groupdict().get('url', None)
    link = matchobj.groupdict().get('link', None)

    #Not Something Embedly Handles
    if not match(url):
        matchobj.group()

    oembed = get_oembed(url)
    #embed was not found or it's a link type
    if oembed is None or oembed['type'] == 'link':
        return matchobj.group()
    elif oembed['type'] in ['video', 'rich']:
        return u'<div class="embed">%s</div>' % oembed['html']
    elif oembed['type'] == 'photo':
        return u'<div class="embed"><a href="%s" title="%s"><img src="%s"></img></a></div>'% (url,oembed.get('title', ''), oembed['url'])

    #bad type?
    return matchobj.group()

def parse(text):
    """
    Parse a piece of text for bbcodes and insert the correct embed code
    """
    return link_url_re.sub(replace, text, re.M )

class EmbedlyTransform:
    implements(ITransform)

    __name__ = "embedly_transform"

    inputs = ('text/html',)
    output = "text/html"

    def __init__(self, name=None):
        self.config_metadata = {
            'inputs' : ('list', 'Inputs', 'Input(s) MIME type. Change with care.'),
            }
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def __getattr__(self, attr):
        if attr == 'inputs':
            return self.config['inputs']
        if attr == 'output':
            return self.config['output']
        raise AttributeError(attr)

    def convert(self, data, idata, filename=None, **kwargs):
        """Convert data.

        Store the result in idata and return that optional argument
        filename may give the original file name of received data
        additional arguments given to engine's convert, convertTo or
        __call__ are passed back to the transform
        
        The object on which the translation was invoked is available
        as context (default: None)
        """
        context = kwargs.get('context', None)
        if context:
            putils = getToolByName(context, 'plone_utils')
            encoding = putils.getSiteEncoding()
            data = data.decode(encoding)
            text = parse(data)
            text = text.encode(encoding)
        else:
            text = parse(data)
        idata.setData(text)
        return idata


def register():
    return EmbedlyTransform()

def initialize():
    engine = getToolByName(portal, 'portal_transforms')
    engine.registerTransform(register())
