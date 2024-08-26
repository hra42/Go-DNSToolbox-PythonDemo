FROM python:3.9-alpine as builder

WORKDIR /app

# Install build dependencies and libraries required for Arrow and pyarrow
RUN apk add --no-cache \
    build-base \
    cmake \
    git \
    ninja \
    boost-dev \
    brotli-dev \
    bzip2-dev \
    curl-dev \
    gflags-dev \
    glog-dev \
    grpc-dev \
    lz4-dev \
    openssl-dev \
    protobuf-dev \
    rapidjson-dev \
    re2-dev \
    snappy-dev \
    thrift-dev \
    utf8proc-dev \
    zlib-dev \
    zstd-dev

# Clone and build Apache Arrow
RUN git clone https://github.com/apache/arrow.git && \
    cd arrow/cpp && \
    mkdir build && \
    cd build && \
    cmake .. -GNinja \
        -DARROW_DEPENDENCY_SOURCE=SYSTEM \
        -DARROW_BUILD_TESTS=OFF \
        -DARROW_PARQUET=ON \
        -DARROW_PYTHON=ON \
        -DARROW_SIMD_LEVEL=NONE \
        -DARROW_RUNTIME_SIMD_LEVEL=NONE && \
    ninja install && \
    cd ../../.. && \
    rm -rf arrow

# Set environment variables for pyarrow
ENV PYARROW_WITH_PARQUET=1 \
    PYARROW_CMAKE_OPTIONS="-DARROW_SIMD_LEVEL=NONE -DARROW_RUNTIME_SIMD_LEVEL=NONE" \
    ARROW_HOME=/usr/local \
    PARQUET_HOME=/usr/local

# Copy and install Python requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Start a new stage for the final image
FROM python:3.9-alpine

WORKDIR /app

# Copy installed packages and Arrow libraries from builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Install runtime dependencies
RUN apk add --no-cache \
    libstdc++ \
    curl \
    git

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
