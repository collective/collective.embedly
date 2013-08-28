from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory(u"collective.embedly")


class IEmbedlySettings(Interface):
    """
    Settings for the Embedly transform
    """

    api_key = schema.TextLine(
        title=_(u"API Key"),
        description=_(
            u"Enter the API key given to you by Embedly. It can be found by "
            u"logging into Embedly and going to your dashboard."
        ),
        required=False,
    )

    use_services_regexp = schema.Bool(
        title=_(u"Use services regexp"),
        description=_(
            u"Use Embedly Services API for checking url before getting "
            u"oembed result."
        ),
        default=True,
        required=False,
    )

    persistent_cache = schema.Bool(
        title=_(u"Use persistent cache"),
        description=_(
            u"Use persistent cache for Embedly Services API call's responses."
        ),
        default=False,
        required=False,
    )

    cache_timeout = schema.Int(
        title=_(u"Cache timeout"),
        description=_(u"Time is seconds to invalidate cache."),
        default=60 * 60 * 24,
        required=False,
    )
