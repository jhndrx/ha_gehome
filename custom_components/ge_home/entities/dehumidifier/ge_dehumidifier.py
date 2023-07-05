import logging

from homeassistant.components.humidifier import HumidifierDeviceClass
from ...devices import ApplianceApi
from ..common import GeHumidifier
from .fan_mode_options import DehumidifierFanModeOptionsConverter

_LOGGER = logging.getLogger(__name__)


class GeDehumidifier(GeHumidifier):
    """Class for Dehumidfiers"""

    def __init__(self, api: ApplianceApi):
        super().__init__(
            api, HumidifierDeviceClass, DehumidifierFanModeOptionsConverter
        )
