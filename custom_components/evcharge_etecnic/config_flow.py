"""Flow de configuración para EVcharge (Etecnic)."""
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION_NAME, DOMAIN, URL_INDEX


class EVchargeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial cuando el usuario añade la integración."""
        errors = {}

        if user_input is not None:
            station_name = user_input[CONF_STATION_NAME].strip()

            # Comprobar que no esté ya añadido
            await self.async_set_unique_id(station_name.lower())
            self._abort_if_unique_id_configured()

            # Validar que el cargador existe en el JSON
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(URL_INDEX) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        # Buscar coincidencia (ignorando mayúsculas/minúsculas o espacios)
                        found = any(
                            station_name.lower() in item.get("name", "").lower()
                            for item in data
                        )
                        if found:
                            return self.async_create_entry(
                                title=station_name,
                                data={CONF_STATION_NAME: station_name},
                            )
                        else:
                            errors["base"] = "not_found"
                    else:
                        errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_STATION_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
