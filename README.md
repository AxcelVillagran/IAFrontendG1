
# Escaneo de Red y Detección de Malware

## Descripción

Este proyecto proporciona una interfaz gráfica de usuario (GUI) diseñada para sistemas Windows que permite a los usuarios escanear su red local y detectar posibles ataques de malware. La aplicación utiliza un modelo de Inteligencia Artificial (GBM) en el backend para analizar los paquetes de red capturados y predecir si los ataques son malignos o benignos.

## Características

- **Escanear Red:** Al presionar el botón "Escanear Red", la aplicación captura paquetes de datos de la red local.
- **Detectar Malware:** Luego de capturar los paquetes, al presionar el botón "Detectar Malware", los datos se envían al backend para que el modelo GBM realice la predicción y determine si hay ataques malignos o benignos.
- **Resultados:** La interfaz gráfica muestra los resultados de la predicción, indicando si se han detectado ataques malignos o benignos.

## Requisitos del Sistema

- **Sistema Operativo:** Windows 7 o superior
- **Framework:** .NET Framework 4.8 o superior
- **Dependencias:** Asegúrate de tener instaladas todas las dependencias necesarias para ejecutar el script necesario para la obtencion de los paquetes (Python, scapy, pandas, joblib).


## Uso

1. **Iniciar la Aplicación:**
   - Haz doble clic en el ejecutable para abrir la interfaz gráfica.

2. **Escanear la Red:**
   - Presiona el botón "Escanear Red" para capturar los paquetes de red.

3. **Detectar Malware:**
   - Una vez completado el escaneo, presiona el botón "Detectar Malware". La aplicación enviará los datos al backend, donde el modelo GBM realizará la predicción.

4. **Ver los Resultados:**
   - La interfaz mostrará si los datos obtenidos son malignos o benignos.

