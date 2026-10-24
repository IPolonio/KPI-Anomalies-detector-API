# 1. Usamos la imagen oficial de Astral que ya trae Python y uv preinstalados
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /code

# 3. Copiamos los archivos de dependencias primero (pyproject.toml y uv.lock)
COPY pyproject.toml uv.lock ./

# 4. Instalamos/sincronizamos las dependencias con uv
RUN uv sync --frozen --no-dev

# 5. Copiamos el resto de tu código de la API
COPY . /code

# 6. Comando para encender tu aplicación
CMD ["uv", "run", "fastapi", "run", "API.py", "--port", "80"]