import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
num_accounts = 500

# --- STEP 1: DATA GENERATE KARNA ---
accounts_data = []
for i in range(num_accounts):
    accounts_data.append({
        'account_id': f'ACC{1000+i}',
        'account_name': fake.company(),
        'industry': random.choice(['DevTools', 'EdTech', 'SaaS', 'FinTech']),
        'country': fake.country_code(),
        'signup_date': fake.date_between(start_date='-2y', end_date='today'),
        'plan_tier': random.choice(['Basic', 'Pro', 'Enterprise']),
        'referral_source': random.choice(['organic', 'ads', 'event', 'partner'])
    })
df_accounts = pd.DataFrame(accounts_data)

usage_data = []
for _ in range(5000):
    usage_data.append({
        'account_id': f'ACC{random.randint(1000, 1499)}',
        'usage_count': random.randint(1, 100)
    })
df_usage = pd.DataFrame(usage_data)

# --- STEP 2: DATA(JOIN) ---
# Har account ka total usage nikal kar accounts ke saath jor dein
usage_sum = df_usage.groupby('account_id')['usage_count'].sum().reset_index()
final_data = pd.merge(df_accounts, usage_sum, on='account_id', how='left').fillna(0)

# --- STEP 3: DESKTOP SAVE ---
desktop_path = r'C:\Users\DELL\Desktop\powerbi_final_data.csv'
final_data.to_csv(desktop_path, index=False)
