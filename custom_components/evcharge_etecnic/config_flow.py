"""Flow de configuración para EVcharge (Etecnic)."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION_ID, CONF_STATION_NAME, DOMAIN, URL_INDEX


class EVchargeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración."""

    VERSION = 1

    def __init__(self):
        """Inicializamos variables temporales."""
        self.search_results = []

    async def async_step_user(self, user_input=None):
        """Paso inicial cuando el usuario añade la integración."""
        errors = {}

        if user_input is not None:
            user_selection = user_input.get(CONF_STATION_NAME, "").strip()

            target_item = None
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(URL_INDEX) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)

                        # 1. Si es un número exacto (ID directo, ej: "83")
                        if user_selection.isdigit():
                            for item in data:
                                if str(item.get("id")) == user_selection:
                                    target_item = item
                                    break

                        # 2. Si no es un número, buscar por nombre exacto
                        if not target_item:
                            for item in data:
                                if item.get("name", "").strip().lower() == user_selection.lower():
                                    target_item = item
                                    break

                        # 3. Si no hay coincidencia exacta, buscar si es texto parcial para el desplegable
                        if not target_item:
                            self.search_results = [
                                item for item in data
                                if user_selection.lower() in item.get("name", "").lower()
                                or user_selection.lower() in item.get("address", "").lower()
                            ]

                            if self.search_results:
                                return await self.async_step_select_station()
                            else:
                                errors["base"] = "not_found"
                    else:
                        errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

            # Fuera del bloque de red, si ya encontramos la estación, validamos el duplicado de forma nativa
            if target_item and not errors:
                station_id = str(target_item.get("id"))
                station_name = target_item.get("name", user_selection)

                await self.async_set_unique_id(f"evcharge_{station_id}")
                self._abort_if_unique_id_configured()  # Esto abortará limpiamente si ya existe

                return self.async_create_entry(
                    title=station_name,
                    data={
                        CONF_STATION_NAME: station_name,
                        CONF_STATION_ID: station_id,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_STATION_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def async_step_select_station(self, user_input=None):
        """Paso secundario: Mostrar desplegable si hay varias coincidencias de texto."""
        errors = {}

        if user_input is not None:
            selected_id_str = user_input[CONF_STATION_ID]
            target_item = next(
                (item for item in self.search_results if str(item.get("id")) == selected_id_str),
                None
            )

            if target_item:
                station_id = str(target_item.get("id"))
                station_name = target_item.get("name", f"Estación {station_id}")

                await self.async_set_unique_id(f"evcharge_{station_id}")
                self._abort_if_unique_id_configured()  # Validación limpia de duplicados

                return self.async_create_entry(
                    title=station_name,
                    data={
                        CONF_STATION_NAME: station_name,
                        CONF_STATION_ID: station_id,
                    },
                )

        from homeassistant.helpers.selector import (
            SelectOptionDict,
            SelectSelector,
            SelectSelectorConfig,
            SelectSelectorMode,
        )

        station_options = [
            SelectOptionDict(
                value=str(station.get("id")),
                label=f"{station.get('name')} — {station.get('address', 'Sin dirección')}"
            )
            for station in self.search_results
        ]

        schema = vol.Schema(
            {
                vol.Required(CONF_STATION_ID): SelectSelector(
                    SelectSelectorConfig(
                        options=station_options,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="select_station",
            data_schema=schema,
            errors=errors,
        )
        schema = vol.Schema(
            {
                vol.Required(CONF_STATION_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
