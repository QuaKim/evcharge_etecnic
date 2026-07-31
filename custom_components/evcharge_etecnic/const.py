"""Constantes para la integración EVcharge (Etecnic)."""

DOMAIN = "evcharge_etecnic"
URL_INDEX = "https://etecnic.net/api/v1/chargers/index.json"

CONF_STATION_NAME = "station_name"
CONF_STATION_ID = "station_id"

STATUS_MAP = {
    0: "Disponible",
    1: "Ocupado",
    3: "Fuera de Servicio",
    9: "No disponible" 
}

CONNECTOR_TYPES = {
    1: "CHAdeMO",
    2: "Type 2 (Mennekes)",
    3: "CCS2",
    5: "Schuko (Doméstico)",
}

# Iconos MDI según el tipo de conector
CONNECTOR_ICONS = {
    1: "mdi:ev-plug-chademo",
    2: "mdi:ev-plug-type2",
    3: "mdi:ev-plug-ccs2",
    5: "mdi:power-socket-eu",
}
