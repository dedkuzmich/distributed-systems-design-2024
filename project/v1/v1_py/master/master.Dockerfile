# Build stage
FROM python:alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:alpine AS final
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .
CMD python ./master.py -p ${PORT}
