import logging
from typing import Coroutine, Any, Optional

from homeassistant.components.humidifier import HumidifierEntity, HumidifierDeviceClass

from gehomesdk import ErdCode, ErdCodeType, ErdOnOff
from homeassistant.components.humidifier.const import HumidifierEntityFeature
from ...const import DOMAIN
from ...devices import ApplianceApi
from .ge_erd_entity import GeEntity
from .options_converter import OptionsConverter

_LOGGER = logging.getLogger(__name__)


class GeHumidifier(GeEntity, HumidifierEntity):
    """GE Humidifier Base Entity (Humidifier and Dehumidifier)"""

    def __init__(
        self,
        api: ApplianceApi,
        device_class: HumidifierDeviceClass,
        fan_mode_converter: OptionsConverter,
        power_status_erd_code: ErdCodeType = ErdCode.AC_POWER_STATUS,
        fan_mode_erd_code: ErdCodeType = ErdCode.AC_FAN_SETTING,
        target_humidity_erd_code: ErdCodeType = ErdCode.DHUM_TARGET_HUMIDITY,
        current_humidity_erd_code: ErdCodeType = ErdCode.DHUM_CURRENT_HUMIDITY,
    ):
        super().__init__(api)
        self._device_class = device_class
        self._fan_mode_converter = fan_mode_converter
        self._power_status_erd_code = api.appliance.translate_erd_code(
            power_status_erd_code
        )
        self._fan_mode_erd_code = api.appliance.translate_erd_code(fan_mode_erd_code)
        self._target_humidity_erd_code = api.appliance.translate_erd_code(
            target_humidity_erd_code
        )
        self._current_humidity_erd_code = api.appliance.translate_erd_code(
            current_humidity_erd_code
        )

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self.serial_or_mac}_{self._device_class}"

    @property
    def name(self) -> Optional[str]:
        return f"{self.serial_or_mac} {self._device_class.title()}"

    @property
    def power_status_erd_code(self):
        return self._power_status_erd_code

    @property
    def fan_mode_erd_code(self):
        return self._fan_mode_erd_code

    @property
    def target_humidity_erd_code(self):
        return self._target_humidity_erd_code

    @property
    def current_humidity_erd_code(self):
        return self._current_humidity_erd_code

    @property
    def target_humidity(self) -> int | None:
        return int(self.appliance.get_erd_value(self.target_humidity_erd_code))

    @property
    def current_humidity(self) -> int | None:
        return int(self.appliance.get_erd_value(self.current_humidity_erd_code))

    @property
    def min_humidity(self) -> int:
        return 35

    @property
    def max_humidity(self) -> int:
        return 80

    @property
    def supported_features(self) -> HumidifierEntityFeature:
        # TODO: Add Non-stop capability as a mode and support it
        return HumidifierEntityFeature(0)

    @property
    def is_on(self) -> bool:
        return self.appliance.get_erd_value(self.power_status_erd_code) == ErdOnOff.ON

    @property
    def device_class(self):
        return self.device_class

    async def async_set_humidity(self, humidity: int) -> Coroutine[Any, Any, None]:
        if self.target_humidity == humidity:
            return

        _LOGGER.debug(
            f"Setting Target Humidity from {self.target_humidity} to {humidity}"
        )

        # if it's not on, turn it on
        if not self.is_on:
            await self.appliance.async_set_erd_value(
                self.power_status_erd_code, ErdOnOff.ON
            )
        # then set the mode
        await self.appliance.async_set_erd_value(
            self.target_humidity_erd_code,
            self.humidity,
        )

    async def async_turn_on(self):
        await self.appliance.async_set_erd_value(
            self.power_status_erd_code, ErdOnOff.ON
        )

    async def async_turn_off(self):
        await self.appliance.async_set_erd_value(
            self.power_status_erd_code, ErdOnOff.OFF
        )
