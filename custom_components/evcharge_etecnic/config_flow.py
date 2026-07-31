"""Config flow para la integración EVcharge (Etecnic)."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_STATION_ID, CONF_STATION_NAME

_LOGGER = logging.getLogger(__name__)


class EtecnicConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Manejar el flujo de configuración para EVcharge (Etecnic)."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial cuando el usuario añade la integración."""
        errors = {}

        if user_input is not None:
            # Comprobar si esta estación ya está añadida para evitar duplicados
            await self.async_set_unique_id(str(user_input[CONF_STATION_ID]))
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_STATION_NAME],
                data={
                    CONF_STATION_ID: user_input[CONF_STATION_ID],
                    CONF_STATION_NAME: user_input[CONF_STATION_NAME],
                },
            )

        # Formulario para solicitar los datos al usuario (o desplegable)
        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATION_ID): int,
                vol.Required(CONF_STATION_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
