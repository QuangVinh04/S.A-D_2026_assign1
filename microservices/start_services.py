#!/usr/bin/env python
"""
Start All Microservices Script
Usage: python start_services.py
"""
import subprocess
import time
import os
import sys
import signal
from pathlib import Path

# Get base directory
BASE_DIR = Path(__file__).parent.resolve()

# Service configurations
SERVICES = [
    {
        'name': 'Customer Service',
        'path': BASE_DIR / 'customer_service',
        'port': 8001,
    },
    {
        'name': 'Book Service',
        'path': BASE_DIR / 'book_service',
        'port': 8002,
    },
    {
        'name': 'Cart Service',
        'path': BASE_DIR / 'cart_service',
        'port': 8003,
    }
]

processes = []

def start_service(service):
    """Start a single service"""
    print(f"Starting {service['name']} on port {service['port']}...")
    
    os.chdir(service['path'])
    
    process = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', str(service['port'])],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=service['path']
    )
    
    return {
        'name': service['name'],
        'process': process,
        'port': service['port']
    }

def stop_all_services():
    """Stop all running services"""
    print("\nStopping all services...")
    for item in processes:
        try:
            item['process'].terminate()
            item['process'].wait(timeout=5)
            print(f"✓ Stopped {item['name']}")
        except subprocess.TimeoutExpired:
            item['process'].kill()
            print(f"✓ Killed {item['name']}")
        except Exception as e:
            print(f"✗ Error stopping {item['name']}: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    stop_all_services()
    sys.exit(0)

def main():
    """Main function"""
    print("=" * 50)
    print("Starting Bookstore Microservices")
    print("=" * 50)
    print()
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start all services
    for service in SERVICES:
        item = start_service(service)
        processes.append(item)
        time.sleep(2)  # Wait between starts
    
    print()
    print("=" * 50)
    print("All services started!")
    print("=" * 50)
    print()
    print("Service URLs:")
    print(f"  Customer Service: http://localhost:8001")
    print(f"  Book Service:     http://localhost:8002")
    print(f"  Cart Service:     http://localhost:8003")
    print()
    print("API Endpoints:")
    print("  Customer Register: POST http://localhost:8001/api/v1/customers/register/")
    print("  Customer Login:    POST http://localhost:8001/api/v1/customers/login/")
    print("  Book Catalog:      GET  http://localhost:8002/api/v1/books/catalog/")
    print("  View Cart:         GET  http://localhost:8003/api/v1/carts/customer/{{customer_id}}/")
    print("  Add to Cart:       POST http://localhost:8003/api/v1/carts/customer/{{customer_id}}/add/")
    print()
    print("Press Ctrl+C to stop all services...")
    print()
    
    # Wait for all processes
    try:
        while True:
            # Check if any process has died
            for item in processes:
                if item['process'].poll() is not None:
                    print(f"Warning: {item['name']} has stopped!")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_all_services()

if __name__ == '__main__':
    main()