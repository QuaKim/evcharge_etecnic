"""Constantes para la integración EVcharge (Etecnic)."""

DOMAIN = "evcharge_etecnic"
URL_INDEX = "https://etecnic.net/api/v1/chargers/index.json"

CONF_STATION_NAME = "station_name"
CONF_STATION_ID = "station_id"

STATUS_MAP = {
    0: "Disponible",
    1: "Ocupado",
    9: "No disponible"
}                                data={
                                    CONF_STATION_ID: station_id,
                                    CONF_STATION_NAME: station_name,
                                },
                            )
                        else:
                            errors["base"] = "not_found"
                    else:
                        errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.error("Error en config_flow de EVcharge: %s", err)
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_STATION_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
