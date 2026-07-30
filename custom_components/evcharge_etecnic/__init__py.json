"""Inicialización de la integración EVcharge (Etecnic)."""
from datetime import timedelta
import logging
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, URL_INDEX

_LOGGER = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura la integración desde una entrada de configuración."""
    session = async_get_clientsession(hass)

    async def async_update_data():
        """Descarga el JSON general de cargadores."""
        try:
            async with session.get(URL_INDEX, headers=HEADERS, timeout=15) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error HTTP: {response.status}")
                return await response.json(content_type=None)
        except Exception as err:
            raise UpdateFailed(f"Error de conexión con Etecnic: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="evcharge_etecnic_coordinator",
        update_method=async_update_data,
        update_interval=timedelta(minutes=3),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Elimina la entrada cuando se borra el dispositivo."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
