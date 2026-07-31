"""Inicialización de la integración EVcharge (Etecnic)."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
# Asumiendo que tu clase Coordinator está en un archivo coordinator.py
from .coordinator import EtecnicDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# Definimos las plataformas que vamos a cargar
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurar EVcharge desde una entrada creada por el usuario (Config Flow)."""
    hass.data.setdefault(DOMAIN, {})

    # 1. Instanciar el Coordinator para las peticiones a la API
    coordinator = EtecnicDataUpdateCoordinator(hass, entry)

    # 2. Hacer la primera llamada a la API antes de cargar nada
    # Esto asegura que tengamos datos listos cuando los sensores se creen
    await coordinator.async_config_entry_first_refresh()

    # 3. Guardar el coordinator en la memoria de HA
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # 4. CARGA DINÁMICA: Envía la señal a HA para que cargue sensor.py INMEDIATAMENTE
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descargar una entrada al eliminar el cargador de Home Assistant."""
    # Descarga las plataformas (elimina los sensores dinámicamente)
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)
    
    # Limpia los datos de memoria
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
