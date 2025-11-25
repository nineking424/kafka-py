"""
Kafka Producer - Sends messages to a Kafka topic
"""
from kafka import KafkaProducer
import json
import time
import argparse

def create_producer(bootstrap_servers='localhost:9092'):
    """Create and configure Kafka producer"""
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        request_timeout_ms=30000,
        max_block_ms=60000,
        retries=5,
        retry_backoff_ms=500,
        metadata_max_age_ms=30000
    )
    return producer

def send_message(producer, topic, key, value):
    """Send a message to Kafka topic"""
    try:
        future = producer.send(topic, key=key, value=value)
        record_metadata = future.get(timeout=10)
        print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Kafka Producer - Send messages to a Kafka topic')
    parser.add_argument(
        '--bootstrap-servers',
        default='localhost:9092',
        help='Kafka bootstrap servers (default: localhost:9092)'
    )
    parser.add_argument(
        '--topic',
        default='test-topic',
        help='Kafka topic name (default: test-topic)'
    )
    parser.add_argument(
        '--num-messages',
        type=int,
        default=10,
        help='Number of messages to send (default: 10)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between messages in seconds (default: 1.0)'
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Display configuration
    print("=== Kafka Producer Configuration ===")
    print(f"Bootstrap Servers: {args.bootstrap_servers}")
    print(f"Topic: {args.topic}")
    print(f"Number of Messages: {args.num_messages}")
    print(f"Delay: {args.delay}s")
    print("====================================\n")

    # Create producer
    print("Creating Kafka producer...")
    producer = create_producer(args.bootstrap_servers)

    try:
        # Send sample messages
        for i in range(args.num_messages):
            message = {
                'id': i,
                'message': f'Hello Kafka {i}',
                'timestamp': time.time()
            }
            key = f'key-{i}'

            print(f"Sending message {i}: {message}")
            send_message(producer, args.topic, key, message)
            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.flush()
        producer.close()
        print("Producer closed")

if __name__ == '__main__':
    main()
