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
    4: "Type 1 (Yazaki)",
    5: "Schuko (Doméstico)",
    6: "Industrial (CETAC)",
    7: "Tesla / NACS",
}

CONNECTOR_ICONS = {
    1: "mdi:ev-plug-chademo",
    2: "mdi:ev-plug-type2",
    3: "mdi:ev-plug-ccs2",
    4: "mdi:ev-plug-type1",
    5: "mdi:power-socket-eu",
    6: "mdi:power-plug",
    7: "mdi:ev-plug-tesla",
