"""Constantes para la integración EVcharge (Etecnic)."""

DOMAIN = "evcharge_etecnic"
URL_INDEX = "https://etecnic.es/mapa-de-recarga/index.json"
CONF_STATION_NAME = "station_name"

STATUS_MAP = {
    0: "Disponible",
    1: "Ocupado",
    9: "No disponible"
}
