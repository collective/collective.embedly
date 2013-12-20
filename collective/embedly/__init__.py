# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

embedlyMessageFactory = MessageFactory(u"collective.embedly")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
