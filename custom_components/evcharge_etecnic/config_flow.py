"""Plataforma de sensores para EVcharge (Etecnic)."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, STATUS_MAP

# Asegúrate de importar o definir CONF_STATION_ID
CONF_STATION_ID = "station_id"
CONF_STATION_NAME = "station_name"


async def async_setup_entry(hass, entry, async_add_entities):
    """Añade los sensores basados en el cargador elegido."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Leemos el ID y el Nombre guardados en la entrada de configuración
    station_id = str(entry.data.get(CONF_STATION_ID, ""))
    station_name = entry.data.get(CONF_STATION_NAME, "")

    entities = []

    # 1. Buscar la estación por ID (o por Nombre como fallback si venías de una versión antigua)
    station_data = None
    for item in coordinator.data or []:
        item_id = str(item.get("id", ""))
        item_name = item.get("name", "").strip().lower()

        # Prioridad absoluta: buscar por ID único
        if station_id and item_id == station_id:
            station_data = item
            break
        # Fallback: si no hay ID guardado, buscar por coincidencia exacta de nombre
        elif not station_id and item_name == station_name.strip().lower():
            station_data = item
            break

    # 2. Crear entidades solo si encontramos los datos del cargador
    if station_data:
        # Sensor principal de la estación (Estado Global)
        entities.append(EVchargeStationSensor(coordinator, entry, station_data))

        # Sensores individuales por cada toma / socket
        for socket in station_data.get("charger_sockets", []):
            socket_num = socket.get("socket_number", 1)
            entities.append(
                EVchargeSocketSensor(coordinator, entry, station_data, socket_num)
            )

    async_add_entities(entities)


class EVchargeBaseSensor(CoordinatorEntity, SensorEntity):
    """Clase base para todos los sensores de EVcharge."""

    def __init__(self, coordinator, entry, station_data):
        super().__init__(coordinator)
        self._entry = entry
        self._station_id = str(station_data.get("id"))
        self._station_name = station_data.get("name", "Cargador EV")
        
        # Cálculo de la potencia real en kW
        self._power_kw = self._calculate_kw(station_data)

    def _calculate_kw(self, station_data):
        """Convierte la intensidad (power en Amperios) y fases a kW reales."""
        if not station_data:
            return None
            
        raw_amps = station_data.get("power", 0)
        phases = station_data.get("phases", 3)
        
        try:
            amps_float = float(raw_amps)
            if amps_float <= 0:
                return None
            return round((amps_float * 230 * phases) / 1000, 1)
        except (ValueError, TypeError):
            return None

    @property
    def device_info(self) -> DeviceInfo:
        """Agrupa automáticamente todas las entidades bajo el mismo Dispositivo."""
        power_str = f" ({self._power_kw} kW)" if self._power_kw else ""
        return DeviceInfo(
            identifiers={(DOMAIN, self._station_id)},
            name=f"EVcharge {self._station_name}{power_str}",
            manufacturer="Etecnic / EVcharge",
            model=f"Punto de Recarga EV{power_str}",
        )

    def _get_station_data(self):
        """Obtiene la información actualizada del cargador desde el coordinador usando el ID."""
        for item in self.coordinator.data or []:
            if str(item.get("id")) == self._station_id:
                return item
        return None


class EVchargeStationSensor(EVchargeBaseSensor):
    """Sensor principal del estado global del cargador."""

    def __init__(self, coordinator, entry, station_data):
        super().__init__(coordinator, entry, station_data)
        self._attr_name = f"Estado Global ({self._power_kw} kW)" if self._power_kw else "Estado Global"
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
            "max_amps": data.get("power"),
            "calculated_power_kw": self._power_kw,
            "phases": data.get("phases"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "sockets_count": len(data.get("charger_sockets", [])),
        }


class EVchargeSocketSensor(EVchargeBaseSensor):
    """Sensor para cada toma de corriente independiente."""

    def __init__(self, coordinator, entry, station_data, socket_num):
        super().__init__(coordinator, entry, station_data)
        self._socket_num = socket_num
        self._attr_name = f"Toma {socket_num}"
        self._attr_unique_id = f"evcharge_{self._station_id}_socket_{socket_num}"
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
