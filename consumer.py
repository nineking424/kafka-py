"""
Kafka Consumer - Receives messages from a Kafka topic
"""
from kafka import KafkaConsumer
import json
import argparse

def create_consumer(topic, bootstrap_servers='localhost:9092', group_id='my-group', auto_offset_reset='earliest'):
    """Create and configure Kafka consumer"""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None
    )
    return consumer

def consume_messages(consumer):
    """Consume messages from Kafka topic"""
    print("Starting to consume messages... (Press Ctrl+C to stop)")
    try:
        for message in consumer:
            print(f"\n--- New Message ---")
            print(f"Topic: {message.topic}")
            print(f"Partition: {message.partition}")
            print(f"Offset: {message.offset}")
            print(f"Key: {message.key}")
            print(f"Value: {message.value}")
            print(f"Timestamp: {message.timestamp}")

    except KeyboardInterrupt:
        print("\n\nStopping consumer...")
    finally:
        consumer.close()
        print("Consumer closed")

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Kafka Consumer - Receive messages from a Kafka topic')
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
        '--group-id',
        default='my-consumer-group',
        help='Consumer group ID (default: my-consumer-group)'
    )
    parser.add_argument(
        '--offset-reset',
        default='earliest',
        choices=['earliest', 'latest'],
        help='Offset reset strategy (default: earliest)'
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Display configuration
    print("=== Kafka Consumer Configuration ===")
    print(f"Bootstrap Servers: {args.bootstrap_servers}")
    print(f"Topic: {args.topic}")
    print(f"Group ID: {args.group_id}")
    print(f"Offset Reset: {args.offset_reset}")
    print("====================================\n")

    # Create consumer
    print(f"Creating Kafka consumer for topic '{args.topic}'...")
    consumer = create_consumer(args.topic, args.bootstrap_servers, args.group_id, args.offset_reset)

    # Start consuming
    consume_messages(consumer)

if __name__ == '__main__':
    main()
