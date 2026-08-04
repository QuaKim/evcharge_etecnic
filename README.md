[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/hacs/integration)
[![Hacs Validation](https://github.com/QuaKim/evcharge_etecnic/actions/workflows/hacs.yml/badge.svg)](https://github.com/QuaKim/evcharge_etecnic/actions/workflows/hacs.yml)
[![GitHub Release](https://img.shields.io/github/v/release/QuaKim/evcharge_etecnic?style=flat-square)](https://github.com/QuaKim/evcharge_etecnic/releases)
[![Total Downloads](https://img.shields.io/github/downloads/QuaKim/evcharge_etecnic/total?style=flat-square)](https://github.com/QuaKim/evcharge_etecnic/releases)
[![License](https://img.shields.io/github/license/QuaKim/evcharge_etecnic?style=flat-square)](https://github.com/QuaKim/evcharge_etecnic/blob/main/LICENSE)

# EVcharge (Etecnic) — Integración para Home Assistant

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

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=QuaKim&repository=evcharge_etecnic&category=integration)

### Opción 1: A través de HACS (Recomendado)

1. Abre **HACS** en el menú lateral de Home Assistant.
2. Haz clic en **Integraciones**.
3. Pulsa el menú de tres puntos `⋮` (arriba a la derecha) y selecciona **Repositorios personalizados**.
4. En **URL**, pega la dirección de tu repositorio en GitHub: https://github.com/QuaKim/evcharge_etecnic/  
5. En **Categoría**, selecciona **Integración**.
6. Haz clic en **Añadir**.
7. Busca **EVcharge (Etecnic)** en la lista de HACS y pulsa **Descargar**.
8. **Reinicia Home Assistant**.

---

### Opción 2: Instalación Manual

1. Descarga la última versión comprimida desde la sección: 
2. Extrae el contenido y copia la carpeta `evcharge` en el directorio `custom_components` de tu servidor de Home Assistant:
   ```text
   config/
   └── custom_components/
       └── evcharge_etecnic/
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


##  ⚙️ Pasos para añadir y configurar Puntos de Carga

Una vez instalada la integración y reiniciado Home Assistant, sigue estos pasos para vincular tu cuenta y añadir tus estaciones:

1. Ve a Ajustes → Dispositivos y servicios.
2. Haz clic en el botón Añadir integración (abajo a la derecha).
3. Busca EVcharge (Etecnic) y selecciónala.

Añadir un punto de carga: 

1. Escribe el Nombre del cargador o su ID de estación, que aparece en la aplicación de Android/iOS, en el campo correspondiente para localizar el punto que deseas vincular.
2. Pulsa Enviar. La integración conectará con la API de EVcharge para añadir la estación.

El cargador aparecerá registrado como un nuevo Dispositivo, identificado con su Nombre, Calle e ID, e incluirá los sensores de sus tomas (Toma 1, Toma 2, etc.).


## 🤝 Contribuciones y Soporte

¡Cualquier reporte de errores, ideas o mejoras son bienvenidos!
Reportar un fallo o sugerencia: Abre un Issue en GitHub.
Aportar código: Envía una Pull Request.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más información
