# Distribución del Agua

Proyecto para analizar y optimizar redes de distribución de agua, incluyendo sectorización, cálculo de flujos máximos, y expansión de redes.

## Requisitos

- Python 3.12 o superior
- [uv](https://github.com/astral-sh/uv) (recomendado) o `venv` para gestión de entornos

## Instalación

### Usando uv (recomendado)

```bash
# Clonar o descargar el repositorio
cd DistribuciondelAgua

# Crear y activar el entorno virtual con uv
uv venv

# Activar el entorno virtual
# En macOS/Linux:
source .venv/bin/activate
# En Windows:
# .venv\Scripts\activate

# Instalar dependencias
uv sync
```

### Usando venv tradicional

```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
# En macOS/Linux:
source .venv/bin/activate
# En Windows:
# .venv\Scripts\activate

# Instalar dependencias
pip install -e .
```

## Ejecución

### Ejecutar el script principal

```bash
# Con uv (recomendado)
uv run python Distribucion_del_Agua.py

# O con Python directamente (después de activar el entorno)
python Distribucion_del_Agua.py
```

### Ejecutar el punto de entrada

```bash
uv run python main.py
```