# Kafka Python Consumer

A simple Kafka consumer implementation using `kafka-python` library.

## Requirements

- Python 3.x
- Apache Kafka

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install kafka-python
```

## Usage

```bash
python consumer.py [OPTIONS]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--bootstrap-servers` | `localhost:9092` | Kafka bootstrap servers |
| `--topic` | `test-topic` | Kafka topic name |
| `--group-id` | `my-consumer-group` | Consumer group ID |
| `--offset-reset` | `earliest` | Offset reset strategy (`earliest` or `latest`) |

### Examples

```bash
# Basic usage with defaults
python consumer.py

# Custom topic and server
python consumer.py --topic my-topic --bootstrap-servers kafka:9092

# Start from latest messages only
python consumer.py --offset-reset latest
```

## Features

- JSON message deserialization
- Configurable consumer group
- Auto commit enabled
- Graceful shutdown with Ctrl+C
