FROM python:3.9-alpine

WORKDIR /app

# Install build dependencies and libraries required for pyarrow
RUN apk add --no-cache \
    build-base \
    curl \
    git \
    cmake \
    pkgconfig \
    python3-dev \
    libffi-dev \
    openssl-dev \
    musl-dev \
    linux-headers \
    libc6-compat

# Set environment variables for pyarrow
ENV PYARROW_WITH_PARQUET=1 \
    PYARROW_CMAKE_OPTIONS="-DARROW_SIMD_LEVEL=NONE -DARROW_RUNTIME_SIMD_LEVEL=NONE"

# Copy and install Python requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
