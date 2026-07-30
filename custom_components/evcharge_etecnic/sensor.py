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
        # Extraemos la potencia global (ej. 50, 22, 100)
        self._power = station_data.get("power", "")

    @property
    def device_info(self) -> DeviceInfo:
        """Agrupa automáticamente todas las entidades bajo el mismo Dispositivo con la potencia en el título."""
        power_str = f" ({self._power} kW)" if self._power else ""
        return DeviceInfo(
            identifiers={(DOMAIN, str(self._station_id))},
            name=f"EVcharge {self._station_name}{power_str}",
            manufacturer="Etecnic / EVcharge",
            model=f"Punto de Recarga EV{power_str}",
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
        # Incluimos la potencia en el nombre de la entidad principal
        power_str = f" {self._power} kW" if self._power else ""
        self._attr_name = f"Estado Global ({self._power} kW)" if self._power else "Estado Global"
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
