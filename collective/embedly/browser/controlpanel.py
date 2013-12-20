from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.form import ControlPanelForm

from collective.embedly import embedlyMessageFactory as _
from collective.embedly.interfaces import IEmbedlySettings


class EmbedlyControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IEmbedlySettings)

    def __init__(self, context):
        super(EmbedlyControlPanelAdapter, self).__init__(context)
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IEmbedlySettings, False)

    def getAPIKey(self):
        return self.settings.api_key

    def setAPIKey(self, value):
        self.settings.api_key = value

    def getUseServicesRegexp(self):
        return self.settings.use_services_regexp

    def setUseServicesRegexp(self, value):
        self.settings.use_services_regexp = value

    def getPersistentCache(self):
        return self.settings.persistent_cache

    def setPersistentCache(self, value):
        self.settings.persistent_cache = value

    def getCacheTimeout(self):
        return self.settings.cache_timeout

    def setCacheTimeout(self, value):
        self.settings.cache_timeout = value

    api_key = property(getAPIKey,
                       setAPIKey)

    use_services_regexp = property(getUseServicesRegexp,
                                   setUseServicesRegexp)

    persistent_cache = property(getPersistentCache,
                                setPersistentCache)

    cache_timeout = property(getCacheTimeout,
                             setCacheTimeout)


class EmbedlyControlPanel(ControlPanelForm):

    label = _("Embedly settings")
    description = _("Lets you change the settings of collective.embedly")
    form_fields = form.FormFields(IEmbedlySettings)
