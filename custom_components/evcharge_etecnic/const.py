"""Constantes para la integración EVcharge (Etecnic)."""

DOMAIN = "evcharge_etecnic"
URL_INDEX = "https://etecnic.net/api/v1/chargers/index.json"

CONF_STATION_NAME = "station_name"
CONF_STATION_ID = "station_id"

STATUS_MAP = {
    0: "Disponible",
    1: "Ocupado",
    3: "Fuera de Servicio"
    9: "No disponible" 
}
