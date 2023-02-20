from collective.embedly import embedlyMessageFactory as _
from collective.embedly.interfaces import IEmbedlySettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from zope.component import getUtility


class EmbedlyControlPanelForm(RegistryEditForm):
    label = _("Embedly settings")
    description = _("Lets you change the settings of collective.embedly")
    schema = IEmbedlySettings


EmbedlyControlPanel = layout.wrap_form(
    EmbedlyControlPanelForm, ControlPanelFormWrapper)