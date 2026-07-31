"""Plataforma de sensores para EVcharge (Etecnic)."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_STATION_ID, CONF_STATION_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configura los sensores a partir de la entrada y el coordinator."""
    # Recuperamos el coordinator que guardó __init__.py
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    station_id = entry.data[CONF_STATION_ID]
    station_name = entry.data[CONF_STATION_NAME]

    # Añadimos el sensor pasando el coordinator
    async_add_entities([EVchargeStatusSensor(coordinator, station_id, station_name)])


class EVchargeStatusSensor(CoordinatorEntity, SensorEntity):
    """Representa el estado del cargador usando el DataUpdateCoordinator."""

    def __init__(self, coordinator, station_id: str, station_name: str) -> None:
        """Inicializa la entidad conectada al coordinator."""
        super().__init__(coordinator)
        self._station_id = str(station_id)
        
        # Propiedades visuales del sensor
        self._attr_name = f"{station_name} Estado"
        self._attr_unique_id = f"evcharge_{station_id}_status"
        self._attr_icon = "mdi:ev-station"

    @property
    def native_value(self) -> str:
        """Devuelve el estado buscando el ID de la estación en los datos del coordinator."""
        if not self.coordinator.data:
            return "Sin datos"

        # Buscamos la estación dentro de la lista devuelta por el JSON
        for item in self.coordinator.data:
            if str(item.get("id")) == self._station_id:
                return item.get("status", "OK")

        return "No encontrada"

    @property
    def extra_state_attributes(self) -> dict:
        """Devuelve atributos adicionales de la estación."""
        if not self.coordinator.data:
            return {}

        for item in self.coordinator.data:
            if str(item.get("id")) == self._station_id:
                return {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "latitude": item.get("lat"),
                    "longitude": item.get("lng"),
                    "connectors": item.get("connectors", []),
                }

        return {}
