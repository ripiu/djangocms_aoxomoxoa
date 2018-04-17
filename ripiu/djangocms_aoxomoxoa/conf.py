from appconf import AppConf

from django.conf import settings  # NOQA
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.templatetags.staticfiles import static

from .item_publishers import item_publishers


class AoxomoxoaAppConf(AppConf):
    # default module name for this app cms plugins
    MODULE_NAME = 'Aoxomoxoa'

    # unite gallery skins
    UNITE_SKINS = (
        ('default', _('Default')),
        ('alexis', _('Alexis')),
    )

    # do I need to load jquery?
    NEEDS_JQUERY = True

    DEFAULT_MEDIA_PICTURE = static("ripiu/djangocms_aoxomoxoa/img/media.svg")

    ITEM_PUBLISHERS = item_publishers

    class Meta:
        prefix = 'ripiu_aoxomoxoa'
