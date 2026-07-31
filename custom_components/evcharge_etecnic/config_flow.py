"""Flow de configuración para EVcharge (Etecnic)."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION_ID, CONF_STATION_NAME, DOMAIN, URL_INDEX


class EVchargeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial cuando el usuario añade la integración."""
        errors = {}

        if user_input is not None:
            user_selection = user_input[CONF_STATION_NAME].strip()

            try:
                session = async_get_clientsession(self.hass)
                async with session.get(URL_INDEX) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        target_item = None

                        # 1. Intentar coincidencia exacta por ID
                        for item in data:
                            if str(item.get("id")) == user_selection:
                                target_item = item
                                break

                        # 2. Intentar coincidencia exacta por nombre
                        if not target_item:
                            for item in data:
                                if item.get("name", "").strip().lower() == user_selection.lower():
                                    target_item = item
                                    break

                        # 3. Fallback: Coincidencia parcial por nombre
                        if not target_item:
                            for item in data:
                                if user_selection.lower() in item.get("name", "").lower():
                                    target_item = item
                                    break

                        if target_item:
                            station_id = str(target_item.get("id"))
                            station_name = target_item.get("name", user_selection)

                            # Evitar duplicados usando el ID propio de la estación
                            await self.async_set_unique_id(f"evcharge_{station_id}")
                            self._abort_if_unique_id_configured()

                            return self.async_create_entry(
                                title=station_name,
                                data={
                                    CONF_STATION_NAME: station_name,
                                    CONF_STATION_ID: station_id,
                                },
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
