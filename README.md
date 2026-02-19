# Gestión de Innovación para el Instituto de Energías Renovables (IER-UNAM)

## Proyecto: Análisis de relaciones entre energía, género y composición familiar

Este repositorio contiene el ecosistema de herramientas desarrollado para el procesamiento, análisis y visualización de datos de la **Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH)**. El objetivo principal es identificar patrones de consumo energético con perspectiva de género mediante técnicas avanzadas de ciencia de datos.

### 🚀 Estructura del Proyecto

El proyecto está organizado de manera modular para separar la lógica de procesamiento de la interfaz de usuario:

* **`scripts/app.py`**: Dashboard interactivo desarrollado en **Streamlit** para la exploración dinámica de resultados.
* **`scripts/paso7_integración_enigh.py`**: Pipeline de limpieza, filtrado y unificación de las bases de datos del INEGI.
* **`scripts/conectar_mysql.py`**: Módulo de gestión de conexión a bases de datos relacionales para el almacenamiento de datos estructurados.

### 🛠️ Metodología Aplicada

El análisis se divide en tres etapas fundamentales documentadas en los entregables del servicio social:

1.  **Reducción de Dimensionalidad (PCA)**: Aplicación de Análisis de Componentes Principales para simplificar la complejidad de las variables socioeconómicas y energéticas.
2.  **Análisis de Redes (NetworkX)**: Identificación de variables estratégicas ("nodos puente") que articulan la relación entre infraestructura básica, localización geográfica y desigualdad energética.
3.  **Visualización Interactiva**: Dashboard con filtros por entidad, sexo del jefe(a) de familia y deciles de ingreso.

### 📦 Gestión de Datos Masivos (+5GB)

Debido al volumen de las bases originales de la ENIGH y los productos intermedios (outputs), este repositorio utiliza una **arquitectura híbrida**:
* **GitHub**: Aloja exclusivamente el código fuente y la lógica del sistema.
* **Google Drive**: Almacena las carpetas `/ENIGH` y `/outputs`. 

> **Nota para ejecución:** Al ejecutar en entornos de nube como Google Colab o GitHub Codespaces, asegúrese de montar su unidad de Google Drive o descargar los CSV correspondientes para que los scripts localicen las rutas de datos.

### 📋 Requisitos e Instalación

Para replicar este entorno localmente o en la nube:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/IER-Dashboard-ENIGH.git](https://github.com/TU_USUARIO/IER-Dashboard-ENIGH.git)# IER-Dashboard-ENIGH
