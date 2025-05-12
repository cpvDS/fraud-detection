import pandas as pd
import random
from faker import Faker
import numpy as np
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

def generate_transaction(i):
    is_fraud = 1 if random.random() < 0.03 else 0

    user_id = random.randint(1000, 9999)
    amount = round(random.uniform(10, 20000), 2)
    country = random.choice(['Kuwait', 'UAE', 'Saudi Arabia'] if not is_fraud else ['Russia', 'Nigeria', 'Iran'])

    login_hour = random.choice([1, 2, 3, 4]) if is_fraud else random.choice(range(8, 22))
    login_time = fake.date_time_this_year().replace(hour=login_hour, minute=random.randint(0, 59), second=0)

    txn_velocity = random.randint(3, 10) if is_fraud else random.randint(0, 2)
    time_since_last = random.randint(0, 30) if is_fraud else random.randint(60, 86400)

    return {
        "transaction_id": i,
        "user_id": user_id,
        "amount": amount,
        "country": country,
        "ip_address": fake.ipv4_public(),
        "device_type": random.choice(["Mobile", "Desktop", "Tablet"]),
        "previous_device_type": random.choice(["Mobile", "Desktop", "Tablet"]),
        "device_id": fake.uuid4(),
        "is_new_device": int(random.random() < 0.7 if is_fraud else random.random() < 0.1),
        "login_time": login_time,
        "previous_location": fake.city(),
        "transaction_type": random.choice(["Online Purchase", "ATM Withdrawal", "Funds Transfer", "POS Payment"]),
        "channel": random.choice(["Mobile App", "Web", "ATM", "POS"]),
        "account_age_days": random.randint(5, 1500),
        "num_failed_logins": random.randint(2, 5) if is_fraud else random.randint(0, 1),
        "txn_velocity_last_hour": txn_velocity,
        "time_since_last_txn_sec": time_since_last,
        "is_foreign_currency": int(is_fraud or random.random() < 0.05),
        "currency": random.choice(["KWD", "USD", "EUR", "CNY"]) if is_fraud else "KWD",
        "merchant_id": fake.uuid4(),
        "merchant_category": random.choice(["Electronics", "Travel", "Gambling", "Luxury Goods", "Groceries"]),
        "is_high_risk_merchant": int(is_fraud and random.choice(["Gambling", "Luxury Goods"]) in ["Gambling", "Luxury Goods"]),
        "card_present": int(random.random() < 0.1 if is_fraud else random.random() < 0.9),
        "login_method": random.choice(["Password", "OTP", "Biometric"]),
        "auth_failure_count_24h": random.randint(3, 10) if is_fraud else random.randint(0, 2),
        "same_ip_multiple_users": int(random.random() < 0.3 if is_fraud else random.random() < 0.05),
        "ip_geolocation_country": country if random.random() > 0.3 else random.choice(["US", "CN", "RU"]),
        "suspicious_keyword_in_desc": int(is_fraud and random.random() < 0.4),
        "tx_time_zone": random.choice(["Asia/Kuwait", "Europe/London", "Asia/Dubai", "UTC"]),
        "device_language": random.choice(["en", "ar", "ru", "zh"]),
        "risk_score": round(random.uniform(70, 100), 1) if is_fraud else round(random.uniform(0, 50), 1),
        "is_fraud": is_fraud
    }

def generate_dataset(filename="full_fraud_dataset.csv", num_rows=10000):
    data = [generate_transaction(i) for i in range(num_rows)]
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Generated {num_rows} transactions -> {filename}")

if __name__ == "__main__":
    generate_dataset()
