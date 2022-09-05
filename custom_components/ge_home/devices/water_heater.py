import logging
from typing import List

from homeassistant.helpers.entity import Entity
from gehomesdk import (
    ErdCode, 
    ErdApplianceType,
    ErdOnOff
)

from custom_components.ge_home.entities.water_heater.ge_water_heater import GeWaterHeater

from .base import ApplianceApi
from ..entities import (
    GeErdSensor, 
    GeErdBinarySensor,
    GeErdSelect,
    GeErdSwitch, 
    ErdOnOffBoolConverter
)

_LOGGER = logging.getLogger(__name__)


class WaterHeaterApi(ApplianceApi):
    """API class for Water Heater objects"""
    APPLIANCE_TYPE = ErdApplianceType.WATER_HEATER

    def get_all_entities(self) -> List[Entity]:
        base_entities = super().get_all_entities()

        wh_entities = [
            GeErdSensor(self, ErdCode.WH_HEATER_TARGET_TEMPERATURE),
            GeErdSensor(self, ErdCode.WH_HEATER_TEMPERATURE),
            GeErdSensor(self, ErdCode.WH_HEATER_MODE_HOURS_REMAINING),
            GeWaterHeater(self)
        ]

        entities = base_entities + wh_entities
        return entities
        
