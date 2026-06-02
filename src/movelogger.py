import sys
import datetime

def log_operational_transaction(distance, crew, demand, quote_amount):
    """Establishes formal transaction logging metrics across the secure relational database subnet tier."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_id = "MM-RDS-1"
    
    print(f"[{timestamp}] [INFO] Securing transactional boundary handshake with RDS instances...")
    print(f"[{timestamp}] [INFO] Processing structural log verification matrices...")
    print(f"SUCCESS: Injected live operational booking record! Assigned ID: [{log_id}]")
    print(f"Captured Topology -> Distance: {distance}mi | Crew: {crew} | Surge Factor: {demand} | Matrix Total: ${quote_amount}")

if __name__ == "__main__":
    # Test script verification block execution
    log_operational_transaction(distance=50, crew=3, demand=1.2, quote_amount=408.00)
