import logging
from typing import List

from homeassistant.helpers.entity import Entity
from gehomesdk.erd import ErdCode, ErdApplianceType

from .base import ApplianceApi
from ..entities import GeErdSensor

_LOGGER = logging.getLogger(__name__)


class DehumidifierApi(ApplianceApi):
    """API class for dehumidifier objects"""

    APPLIANCE_TYPE = ErdApplianceType.DEHUMIDIFIER

    def get_all_entities(self) -> List[Entity]:
        base_entities = super().get_all_entities()

        dehumidifier_entities = [
            GeErdSensor(self, ErdCode.DHUM_CURRENT_HUMIDITY),
            GeErdSensor(self, ErdCode.DHUM_TARGET_HUMIDITY),
            GeErdSensor(self, ErdCode.DHUM_MAINTENANCE),
            GeErdSensor(self, ErdCode.AC_FAN_SETTING, icon_override="mdi:fan"),
            GeErdSensor(self, ErdCode.WAC_DEMAND_RESPONSE_STATE),
            GeErdSensor(self, ErdCode.WAC_DEMAND_RESPONSE_POWER, uom_override="kW"),
        ]

        entities = base_entities + dehumidifier_entities
        return entities
