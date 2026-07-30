"""Plataforma de sensores para EVcharge (Etecnic)."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import CONF_STATION_NAME, DOMAIN, STATUS_MAP


async def async_setup_entry(hass, entry, async_add_entities):
    """Añade los sensores basados en el cargador elegido."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    station_name = entry.data[CONF_STATION_NAME]

    entities = []

    # Buscar la estación en los datos
    station_data = None
    for item in coordinator.data or []:
        if station_name.lower() in item.get("name", "").lower():
            station_data = item
            break

    if station_data:
        # 1. Sensor principal de la estación (Estado Global)
        entities.append(EVchargeStationSensor(coordinator, entry, station_name, station_data))

        # 2. Sensores individuales por cada toma / socket
        for socket in station_data.get("charger_sockets", []):
            socket_num = socket.get("socket_number", 1)
            entities.append(
                EVchargeSocketSensor(coordinator, entry, station_name, station_data, socket_num)
            )

    async_add_entities(entities)


class EVchargeBaseSensor(CoordinatorEntity, SensorEntity):
    """Clase base para todos los sensores de EVcharge."""

    def __init__(self, coordinator, entry, station_name, station_data):
        super().__init__(coordinator)
        self._entry = entry
        self._station_name = station_name
        self._station_id = station_data.get("id", entry.entry_id)

    @property
    def device_info(self) -> DeviceInfo:
        """Agrupa automáticamente todas las entidades bajo el mismo Dispositivo."""
        return DeviceInfo(
            identifiers={(DOMAIN, str(self._station_id))},
            name=f"EVcharge {self._station_name}",
            manufacturer="Etecnic / EVcharge",
            model="Punto de Recarga EV",
        )

    def _get_station_data(self):
        """Obtiene la información actualizada del cargador desde el coordinador."""
        for item in self.coordinator.data or []:
            if self._station_name.lower() in item.get("name", "").lower():
                return item
        return None


class EVchargeStationSensor(EVchargeBaseSensor):
    """Sensor principal del estado global del cargador."""

    def __init__(self, coordinator, entry, station_name, station_data):
        super().__init__(coordinator, entry, station_name, station_data)
        self._attr_name = "Estado Global"
        self._attr_unique_id = f"evcharge_{entry.entry_id}_main"
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
            "power_kw": data.get("power"),
            "phases": data.get("phases"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "sockets_count": len(data.get("charger_sockets", [])),
        }


class EVchargeSocketSensor(EVchargeBaseSensor):
    """Sensor para cada toma de corriente independiente."""

    def __init__(self, coordinator, entry, station_name, station_data, socket_num):
        super().__init__(coordinator, entry, station_name, station_data)
        self._socket_num = socket_num
        self._attr_name = f"Toma {socket_num}"
        self._attr_unique_id = f"evcharge_{entry.entry_id}_socket_{socket_num}"

    def _get_socket_data(self):
        """Obtiene la información específica de esta toma."""
        data = self._get_station_data()
        if data:
            for s in data.get("charger_sockets", []):
                if s.get("socket_number") == self._socket_num:
                    return s
        return None

    @property
    def native_value(self):
        socket = self._get_socket_data()
        if socket:
            return STATUS_MAP.get(socket.get("status"), "Desconocido")
        return "Desconocido"

    @property
    def icon(self):
        """Icono dinámico según estado."""
        socket = self._get_socket_data()
        if socket:
            status = socket.get("status")
            if status == 0:  # Disponible
                return "mdi:power-plug-charging"
            elif status == 1:  # Ocupado
                return "mdi:power-plug-off"
            elif status == 9:  # No disponible / Mantenimiento
                return "mdi:power-plug-outline"
        return "mdi:power-plug"

    @property
    def icon_color(self):
        """Color dinámico según estado para dashboards compatibles (Mushroom, etc.)."""
        socket = self._get_socket_data()
        if socket:
            status = socket.get("status")
            if status == 0:  # Disponible -> Verde
                return "var(--success-color, green)"
            elif status == 1:  # Ocupado -> Rojo
                return "var(--error-color, red)"
            elif status == 9:  # No disponible -> Gris / Naranja
                return "var(--disabled-text-color, grey)"
        return "var(--disabled-text-color, grey)"

    @property
    def extra_state_attributes(self):
        socket = self._get_socket_data()
        if not socket:
            return {}
        return {
            "socket_id": socket.get("id"),
            "connector_type_id": socket.get("connector_type_id"),
        }
