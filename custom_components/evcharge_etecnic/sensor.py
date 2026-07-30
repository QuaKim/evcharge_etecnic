"""Plataforma de sensores para EVcharge (Etecnic)."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
        # Sensor principal de la estación
        entities.append(EVchargeStationSensor(coordinator, entry, station_name))

        # Sensores individuales por cada toma / socket
        for socket in station_data.get("charger_sockets", []):
            socket_num = socket.get("socket_number", 1)
            entities.append(
                EVchargeSocketSensor(coordinator, entry, station_name, socket_num)
            )

    async_add_entities(entities)


class EVchargeBaseSensor(CoordinatorEntity, SensorEntity):
    """Clase base para sensores EVcharge."""

    def __init__(self, coordinator, entry, station_name):
        super().__init__(coordinator)
        self._entry = entry
        self._station_name = station_name

    def _get_station_data(self):
        for item in self.coordinator.data or []:
            if self._station_name.lower() in item.get("name", "").lower():
                return item
        return None


class EVchargeStationSensor(EVchargeBaseSensor):
    """Sensor principal del estado global del cargador."""

    def __init__(self, coordinator, entry, station_name):
        super().__init__(coordinator, entry, station_name)
        self._attr_name = f"EVcharge {station_name}"
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

    def __init__(self, coordinator, entry, station_name, socket_num):
        super().__init__(coordinator, entry, station_name)
        self._socket_num = socket_num
        self._attr_name = f"EVcharge {station_name} - Toma {socket_num}"
        self._attr_unique_id = f"evcharge_{entry.entry_id}_socket_{socket_num}"
        self._attr_icon = "mdi:power-plug-charging"

    @property
    def native_value(self):
        data = self._get_station_data()
        if data:
            sockets = data.get("charger_sockets", [])
            for s in sockets:
                if s.get("socket_number") == self._socket_num:
                    return STATUS_MAP.get(s.get("status"), "Desconocido")
        return "Desconocido"

    @property
    def extra_state_attributes(self):
        data = self._get_station_data()
        if data:
            sockets = data.get("charger_sockets", [])
            for s in sockets:
                if s.get("socket_number") == self._socket_num:
                    return {
                        "socket_id": s.get("id"),
                        "connector_type_id": s.get("connector_type_id"),
                    }
        return {}
