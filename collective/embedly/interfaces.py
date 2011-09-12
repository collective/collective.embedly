from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory(u"collective.embedly")


class IEmbedlySettings(Interface):
    """Settings for the Embedly transform
    """

    api_key = schema.TextLine(
        title=_(u"API Key"),
        description=_(
            u"Enter the API key given to you by Embedly. It can be found by "
            "logging into Embedly and going to your dashboard."
        ),
        required=False,
    )
