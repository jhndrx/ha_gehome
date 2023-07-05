import logging
from typing import Any, List, Optional

from gehomesdk import ErdAcFanSetting
from ..common import OptionsConverter

_LOGGER = logging.getLogger(__name__)

SMART_DRY = "SMART DRY"

class DehumidifierFanModeOptionsConverter(OptionsConverter):
    def __init__(self, default_option: ErdAcFanSetting = ErdAcFanSetting.DEFAULT):
        self._default = default_option
       
    @property
    def options(self) -> List[str]:
        # Default == Smart Dry
        return [SMART_DRY.title()] + [i.stringify() for i in [ErdAcFanSetting.LOW, ErdAcFanSetting.MED, ErdAcFanSetting.HIGH]]
 
    def from_option_string(self, value: str) -> Any:
        if value.upper() == SMART_DRY:
            value = "Default"
        try:
            return ErdAcFanSetting[value.upper().replace(" ","_")]
        except:
            _LOGGER.warn(f"Could not set fan mode to {value}")
            return self._default

    def to_option_string(self, value: Any) -> Optional[str]:
        try:
            return {
                ErdAcFanSetting.DEFAULT: ErdAcFanSetting.DEFAULT,
                ErdAcFanSetting.AUTO: ErdAcFanSetting.DEFAULT,
                ErdAcFanSetting.LOW: ErdAcFanSetting.LOW,
                ErdAcFanSetting.LOW_AUTO: ErdAcFanSetting.LOW,
                ErdAcFanSetting.MED: ErdAcFanSetting.MED,
                ErdAcFanSetting.MED_AUTO: ErdAcFanSetting.MED,
                ErdAcFanSetting.HIGH: ErdAcFanSetting.HIGH,
                ErdAcFanSetting.HIGH_AUTO: ErdAcFanSetting.HIGH
            }.get(value).stringify()
        except:
            pass
        return self._default.stringify()
