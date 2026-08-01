# EVcharge (Etecnic) — Integración para Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/usuario/evcharge-ha?style=flat-square&color=blue)](https://github.com/usuario/evcharge-ha/releases)
[![HACS Default](https://img.shields.io/badge/HACS-Custom-orange.style=flat-square)](https://hacs.xyz/)
[![Validate Domain](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue.svg?style=flat-square)](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/usuario/evcharge-ha?style=flat-square)](LICENSE)

> ⚠️ **Aviso de exención de responsabilidad (Disclaimer)**  
> Esta es una **integración no oficial** desarrollada por la comunidad. No está afiliada, respaldada ni asociada oficialmente con **Etecnic** ni con **EVcharge**.

---

## 🚗 Descripción de la Integración

La integración **EVcharge (Etecnic)** conecta Home Assistant con la plataforma de infraestructura y carga de vehículos eléctricos de Etecnic / EVcharge. 

Es de **gran utilidad para usuarios que hacen un uso frecuente de cargadores públicos o gestionan varias estaciones a la vez**, ya que permite consultar de un solo vistazo el estado global de múltiples puntos de recarga y sus tomas en una misma pantalla, evitando la molestia de tener que navegar uno a uno dentro de la app móvil oficial.

Está pensada para ofrecer una experiencia nativa y limpia, creando **un dispositivo por cada estación de recarga** y agrupando dentro de él sus sensores independientes.

---

## ⚡ Funciones y Funcionalidades

### 1. Monitorización de Estado en Tiempo Real
- **Estado de las tomas:** Consulta al instante si una toma está `Disponible`, `Ocupada / Cargando`, `Reservada`, `Fuera de servicio` o en `Error`.
- **Actualización automática asíncrona:** Polling en segundo plano mediante `DataUpdateCoordinator` para mantener los datos al día sin saturar la red ni ralentizar Home Assistant.

### 2. Gestión Multiestación y Organización Visual
- **Ficha de Dispositivo Completa:** Cada cargador se registra con su **Nombre de estación**, **Dirección / Calle** e **ID de cargador** para identificarlo fácilmente si gestionas varios puntos.
- **Iconos Dinámicos MDI:** Identificación visual del conector (`mdi:ev-plug-ccs2`, `mdi:ev-plug-type2`, `mdi:power-socket-eu`, etc.) según el tipo de toma detectado.
- **Nombres de Entidad Limpios:** Sensores nombrados de forma concisa (`Toma 1`, `Toma 2`) para mantener los `entity_id` breves y fáciles de usar en tarjetas o automatizaciones.

### 3. Atributos Técnicos Detallados
Cada sensor expone en sus atributos información extendida de la toma:
- Tipo de conector (CCS2, Type 2, CHAdeMO, etc.).
- Potencia máxima / disponible (kW).
- Identificadores internos de estación y conector.
- Estado detallado devuelto por la API.

---

## 📸 Capturas de pantalla

| Configuración vía UI | Ficha de Dispositivo y Sensores |
| :---: | :---: |
| ![Configuración UI](https://via.placeholder.com/400x250.png?text=Configuracion+UI+EVcharge) | ![Dashboard Sensores](https://via.placeholder.com/400x250.png?text=Dispositivo+y+Tomas+HA) |

*(Nota: Puedes reemplazar estas imágenes subiendo capturas reales a tu repositorio).*

---

## 📦 Instalación

### Opción 1: A través de HACS (Recomendado)

1. Abre **HACS** en el menú lateral de Home Assistant.
2. Haz clic en **Integraciones**.
3. Pulsa el menú de tres puntos `⋮` (arriba a la derecha) y selecciona **Repositorios personalizados**.
4. En **URL**, pega la dirección de tu repositorio en GitHub:
   `https://github.com/TU_USUARIO/TU_REPOSITORIO`
5. En **Categoría**, selecciona **Integración**.
6. Haz clic en **Añadir**.
7. Busca **EVcharge (Etecnic)** en la lista de HACS y pulsa **Descargar**.
8. **Reinicia Home Assistant**.

---

### Opción 2: Instalación Manual

1. Descarga la última versión comprimida desde la sección [Releases](https://github.com/TU_USUARIO/TU_REPOSITORIO/releases).
2. Extrae el contenido y copia la carpeta `evcharge` en el directorio `custom_components` de tu servidor de Home Assistant:
   ```text
   config/
   └── custom_components/
       └── evcharge/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           └── ...5. En **Categoría**, selecciona **Integración**.
6. Haz clic en **Añadir**.
7. Busca **EVcharge (Etecnic)** en la lista de HACS y pulsa **Descargar**.
8. **Reinicia Home Assistant**.

---

### Opción 2: Instalación Manual

1. Descarga la última versión comprimida desde la sección [Releases](https://github.com/TU_USUARIO/TU_REPOSITORIO/releases).
2. Extrae el contenido y copia la carpeta `evcharge` en el directorio `custom_components` de tu servidor de Home Assistant:
   ```text
   config/
   └── custom_components/
       └── evcharge/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           └── ...
