"""Plataforma de sensores para EVcharge (Etecnic)."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_STATION_NAME, CONNECTOR_ICONS, CONNECTOR_TYPES, DOMAIN, STATUS_MAP

_LOGGER = logging.getLogger(__name__)

try:
    from .const import CONF_STATION_ID
except ImportError:
    CONF_STATION_ID = "station_id"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configura los sensores a partir de la entrada de configuración."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    station_name = entry.data.get(CONF_STATION_NAME, "")
    station_id = entry.data.get(CONF_STATION_ID)

    # Forzamos refresh si por algún motivo coordinator.data viene vacío
    if not coordinator.data:
        await coordinator.async_refresh()

    station_data = None
    for item in coordinator.data or []:
        item_id = str(item.get("id", ""))
        item_name = item.get("name", "").strip()

        if station_id and str(station_id) == item_id:
            station_data = item
            break
        elif station_name and station_name.lower() in item_name.lower():
            station_data = item
            break

    if not station_data:
        _LOGGER.warning(
            "No se encontraron datos en el JSON para la estación: %s (ID: %s)",
            station_name,
            station_id,
        )
        return

    real_id = str(station_data.get("id", entry.entry_id))
    real_name = station_data.get("name", station_name or f"Estación {real_id}")

    entities = []

    # 1. Sensor principal del estado global
    entities.append(
        EVchargeStationSensor(coordinator, entry, real_name, real_id)
    )

    # 2. Sensores por cada toma / socket
    for socket in station_data.get("charger_sockets", []):
        socket_num = socket.get("socket_number", 1)
        connector_type_id = socket.get("connector_type_id")
        
        entities.append(
            EVchargeSocketSensor(
                coordinator, entry, real_name, real_id, socket_num, connector_type_id
            )
        )

    # Registramos entidades al instante
    async_add_entities(entities, update_before_add=False)


class EVchargeBaseSensor(CoordinatorEntity, SensorEntity):
    """Clase base para los sensores de EVcharge."""

    def __init__(
        self, coordinator, entry: ConfigEntry, station_name: str, station_id: str
    ) -> None:
        """Inicializa el sensor base."""
        super().__init__(coordinator)
        self._entry = entry
        self._station_name = station_name
        self._station_id = station_id

    @property
    def device_info(self) -> DeviceInfo:
        """Asigna la entidad al Dispositivo correspondiente en la interfaz."""
        return DeviceInfo(
            identifiers={(DOMAIN, str(self._station_id))},
            name=f"EVcharge {self._station_name}",
            manufacturer="Etecnic / EVcharge",
            model="Punto de Recarga EV",
        )

    def _get_station_data(self):
        """Busca los datos actualizados de la estación en el coordinador."""
        for item in self.coordinator.data or []:
            if str(item.get("id")) == str(self._station_id):
                return item
            elif self._station_name.lower() in item.get("name", "").lower():
                return item
        return None


class EVchargeStationSensor(EVchargeBaseSensor):
    """Sensor principal del estado global del cargador."""

    def __init__(
        self, coordinator, entry: ConfigEntry, station_name: str, station_id: str
    ) -> None:
        super().__init__(coordinator, entry, station_name, station_id)
        self._attr_name = "Estado Global"
        self._attr_unique_id = f"evcharge_{self._station_id}_main"
        self._attr_icon = "mdi:ev-station"

    @property
    def native_value(self):
        data = self._get_station_data()
        if data:
            status_code = data.get("status", 9)
            return STATUS_MAP.get(status_code, "Desconocido")
        return "Desconocido"

    @property
    def extra_state_attributes(self):
        data = self._get_station_data()
        if not data:
            return {}
        return {
            "id": data.get("id"),
            "address": data.get("address"),
            "power_amps": data.get("power"),
            "phases": data.get("phases"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "sockets_count": len(data.get("charger_sockets", [])),
        }


class EVchargeSocketSensor(EVchargeBaseSensor):
    """Sensor para cada toma de corriente independiente."""

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        station_name: str,
        station_id: str,
        socket_num: int,
        connector_type_id: int = None,
    ) -> None:
        super().__init__(coordinator, entry, station_name, station_id)
        self._socket_num = int(socket_num)
        self._connector_type_id = connector_type_id

# Indicaba tipo de connector en entidad.
#        conn_name = CONNECTOR_TYPES.get(connector_type_id) if connector_type_id else None
#        suffix = f" ({conn_name})" if conn_name else ""

        self._attr_name = f"Toma {self._socket_num}{suffix}"
        self._attr_unique_id = f"evcharge_{self._station_id}_socket_{self._socket_num}"

    def _get_socket_data(self):
        """Método auxiliar para obtener la información específica de esta toma."""
        station_data = self._get_station_data()
        if station_data:
            sockets = station_data.get("charger_sockets", [])
            for s in sockets:
                if int(s.get("socket_number", 0)) == self._socket_num:
                    return s
        return None

    @property
    def native_value(self):
        """Devuelve el estado traducido de la toma."""
        socket_data = self._get_socket_data()
        if socket_data is not None:
            status_code = socket_data.get("status")
            return STATUS_MAP.get(status_code, f"Desconocido ({status_code})")
        return "Cargando..."

    @property
    def icon(self):
        """Devuelve el icono adecuado según el tipo de conector."""
        socket_data = self._get_socket_data()
        type_id = self._connector_type_id

        if socket_data and "connector_type_id" in socket_data:
            type_id = socket_data.get("connector_type_id")

        return CONNECTOR_ICONS.get(type_id, "mdi:power-plug-charging")

    @property
    def extra_state_attributes(self):
        """Devuelve los atributos extra de la toma."""
        socket_data = self._get_socket_data()
        if socket_data:
            type_id = socket_data.get("connector_type_id", self._connector_type_id)
            return {
                "socket_id": socket_data.get("id"),
                "connector_type_id": type_id,
                "connector_type": CONNECTOR_TYPES.get(type_id, f"Tipo {type_id}"),
            }
        return {}
