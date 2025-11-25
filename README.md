# Kafka Python Consumer & Producer

A simple Kafka consumer and producer implementation using `kafka-python-ng` library.

## Requirements

- Python 3.x
- Apache Kafka

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Local Usage

### Consumer

```bash
python consumer.py [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--bootstrap-servers` | `localhost:9092` | Kafka bootstrap servers |
| `--topic` | `test-topic` | Kafka topic name |
| `--group-id` | `my-consumer-group` | Consumer group ID |
| `--offset-reset` | `earliest` | Offset reset strategy (`earliest` or `latest`) |

Consumer automatically uses hostname as `client_id` for broker identification.

### Producer

```bash
python producer.py [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--bootstrap-servers` | `localhost:9092` | Kafka bootstrap servers |
| `--topic` | `test-topic` | Kafka topic name |
| `--num-messages` | `10` | Number of messages to send |
| `--delay` | `1.0` | Delay between messages in seconds |

### Examples

```bash
# Consumer with custom settings
python consumer.py --topic my-topic --bootstrap-servers kafka:9092

# Producer sending 100 messages
python producer.py --num-messages 100 --delay 0.5
```

## Kubernetes Deployment

Deploy to Kubernetes without building custom container images using ConfigMap + Init Container pattern.

### Architecture

```
┌─────────────────────────────────────────────────┐
│                    Pod                           │
├─────────────────────────────────────────────────┤
│  [Init Container: python:3.12-slim]             │
│   - pip install --target=/app/lib               │
├─────────────────────────────────────────────────┤
│  [Main Container: python:3.12-slim]             │
│   - PYTHONPATH=/app/lib                         │
│   - python /app/scripts/consumer.py             │
├─────────────────────────────────────────────────┤
│  Volumes:                                        │
│   - scripts (ConfigMap) → /app/scripts          │
│   - python-libs (emptyDir) → /app/lib           │
└─────────────────────────────────────────────────┘
```

### Deploy

```bash
# Deploy all resources
kubectl apply -f k8s/

# Check pod status
kubectl get pods -n kafka-apps

# View logs
kubectl logs -f statefulset/kafka-consumer -n kafka-apps
kubectl logs -f statefulset/kafka-producer -n kafka-apps
```

### Configuration

Edit `k8s/configmap-config.yaml` to change Kafka settings:

```yaml
data:
  KAFKA_BOOTSTRAP_SERVERS: "kafka-broker:9092"
  KAFKA_TOPIC: "test-topic"
  KAFKA_GROUP_ID: "my-consumer-group"
  KAFKA_OFFSET_RESET: "earliest"
  KAFKA_NUM_MESSAGES: "10"
  KAFKA_DELAY: "1.0"
```

### Update Code

```bash
# After modifying Python code, update ConfigMap and restart pods
kubectl apply -f k8s/configmap-scripts.yaml
kubectl rollout restart statefulset/kafka-consumer statefulset/kafka-producer -n kafka-apps
```

### Cleanup

```bash
kubectl delete -f k8s/
```

## Features

- JSON message serialization/deserialization
- Configurable consumer group
- Hostname-based client ID for consumer identification
- Auto commit enabled
- Graceful shutdown with Ctrl+C
- Kubernetes deployment without custom image build
- StatefulSet with parallel pod management
