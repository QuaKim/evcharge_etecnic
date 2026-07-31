"""Plataforma de sensores para EVcharge (Etecnic)."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATUS_MAP, CONNECTOR_TYPES, CONNECTOR_ICONS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar los sensores de Etecnic al instante sin necesidad de reiniciar."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    station_id = entry.data.get("station_id")
    station_name = entry.data.get("station_name")

    entities = []

    # Verificamos que el coordinator tiene datos y contiene la lista de tomas ("sockets")
    if coordinator.data and "sockets" in coordinator.data:
        for socket_data in coordinator.data["sockets"]:
            # Usamos int() por seguridad tal y como detectamos anteriormente
            socket_id = int(socket_data.get("id"))
            
            entities.append(
                EtecnicSocketSensor(
                    coordinator=coordinator,
                    station_id=station_id,
                    station_name=station_name,
                    socket_id=socket_id,
                )
            )

    # Añadimos las entidades a HA. update_before_add=False porque ya hicimos el 
    # async_config_entry_first_refresh en el __init__.py
    async_add_entities(entities)


class EtecnicSocketSensor(CoordinatorEntity, SensorEntity):
    """Sensor que representa una toma individual de un punto de recarga Etecnic."""

    def __init__(self, coordinator, station_id, station_name, socket_id):
        """Inicializar el sensor de la toma."""
        super().__init__(coordinator)
        
        self._station_id = station_id
        self._station_name = station_name
        self._socket_id = int(socket_id)

        # Identificador único interno para Home Assistant
        self._attr_unique_id = f"{DOMAIN}_{station_id}_socket_{self._socket_id}"
        # Nombre visible, ej: "Toma 1", "Toma 1726", etc.
        self._attr_name = f"Toma {self._socket_id}"

    def _get_socket_data(self):
        """Extraer los datos actualizados de esta toma en concreto del coordinator."""
        if not self.coordinator.data or "sockets" not in self.coordinator.data:
            return None
            
        for socket in self.coordinator.data["sockets"]:
            # Comparación robusta basada en enteros
            if int(socket.get("id")) == self._socket_id:
                return socket
                
        return None

    @property
    def native_value(self):
        """Devolver el estado actual de la toma mapeado a texto."""
        data = self._get_socket_data()
        if not data:
            return "Desconocido"
            
        status_id = int(data.get("status", 9))
        return STATUS_MAP.get(status_id, "Desconocido")

    @property
    def icon(self):
        """Devolver el icono MDI dinámico basado en el tipo de conector."""
        data = self._get_socket_data()
        if not data:
            return "mdi:power-plug-charging"
            
        connector_id = int(data.get("connector_type_id", 0))
        return CONNECTOR_ICONS.get(connector_id, "mdi:power-plug-charging")

    @property
    def extra_state_attributes(self):
        """Devolver atributos extra útiles (tipo de conector en texto y su ID)."""
        data = self._get_socket_data()
        if not data:
            return {}
            
        connector_id = int(data.get("connector_type_id", 0))
        return {
            "connector_type_id": connector_id,
            "connector_type": CONNECTOR_TYPES.get(connector_id, f"Tipo {connector_id}"),
        }

    @property
    def device_info(self):
        """Agrupar este sensor bajo el mismo Dispositivo principal (la estación)."""
        return {
            "identifiers": {(DOMAIN, str(self._station_id))},
            "name": self._station_name,
            "manufacturer": "Etecnic / EVcharge",
            "model": "Punto de Recarga EV",
        }
