import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load datasets
accounts = pd.read_csv("data/accounts.csv")
subscriptions = pd.read_csv("data/subscriptions.csv")
feature_usage = pd.read_csv("data/feature_usage.csv")
support_tickets = pd.read_csv("data/support_tickets.csv")
churn_events = pd.read_csv("data/churn_events.csv")

# Show first 5 rows
print(accounts.head())


import pandas as pd

# Load Data
accounts = pd.read_csv("data/accounts.csv")
subs = pd.read_csv("data/subscriptions.csv")

# Analysis: count the accounts
print("--- Industry Distribution ---")
print(accounts['industry'].value_counts())

# Analysis: Average Seats count
print("\n--- Average Seats per Plan ---")
print(accounts.groupby('plan_tier')['seats'].mean())


import matplotlib.pyplot as plt
import seaborn as sns

# Graph size and style
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Industry distribution ka bar chart
sns.countplot(data=accounts, x='industry', palette='viridis')

plt.title('Accounts Distribution by Industry')
plt.xlabel('Industry Type')
plt.ylabel('Number of Accounts')
plt.show()

# join tables according to account_id
merged_df = pd.merge(subs, accounts[['account_id', 'country']], on='account_id')

# Country wise revenue (MRR)  total
country_revenue = merged_df.groupby('country')['mrr_amount'].sum().sort_values(ascending=False).head(10)

print("\n--- Top 10 Countries by Revenue (MRR) ---")
print(country_revenue)

# Making graph
plt.figure(figsize=(12, 6))
country_revenue.plot(kind='bar', color='skyblue')
plt.title('Top 10 Countries by Monthly Recurring Revenue')
plt.ylabel('Total MRR ($)')
plt.xticks(rotation=45)
plt.show()

# Support tickets and join accounts
tickets = pd.read_csv("data/support_tickets.csv")
ticket_analysis = pd.merge(tickets, accounts[['account_id', 'churn_flag']], on='account_id')

# Graph: Satisfaction score's impact on churn
plt.figure(figsize=(10, 6))
sns.countplot(data=ticket_analysis, x='satisfaction_score', hue='churn_flag', palette='magma')

plt.title('Satisfaction Score vs Churn Status')
plt.xlabel('Satisfaction Score (1 = Poor, 5 = Excellent)')
plt.ylabel('Number of Customers')
plt.legend(title='Churned?', labels=['No (Stayed)', 'Yes (Left)'])
plt.show()

usage = pd.read_csv("data/feature_usage.csv")

# according to Feature group the usage
feature_stats = usage.groupby('feature_name')['usage_count'].sum().sort_values(ascending=False)

print("\n--- Most Popular Features ---")
print(feature_stats)

# Visualizing Feature Popularity
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_stats.index, y=feature_stats.values, palette='coolwarm')
plt.title('Total Usage by Feature')
plt.ylabel('Total Times Used')
plt.show()

# Usage and Accounts joining , to know churn's 
usage_with_churn = pd.merge(usage, accounts[['account_id', 'churn_flag']], on='account_id')

# Churn average usage for every feature
churn_usage = usage_with_churn.groupby(['churn_flag', 'feature_name'])['usage_count'].mean().unstack()

print("\n--- Average Feature Usage: Staying vs Leaving ---")
print(churn_usage)

# making Heatmap to instand know the difference
plt.figure(figsize=(10, 6))
sns.heatmap(churn_usage, annot=True, cmap="YlGnBu", fmt='.1f')
plt.title('Average Feature Usage (Churned vs Active)')
plt.ylabel('Is Churned? (False = Stayed, True = Left)')
plt.show()

# 1. merging all the tables 
# Accounts + Subscriptions (Revenue)
summary = pd.merge(accounts[['account_id', 'account_name', 'industry', 'plan_tier']], 
                   subs.groupby('account_id')['mrr_amount'].sum().reset_index(), 
                   on='account_id', how='left')

# + Usage (API and other feature's total)
summary = pd.merge(summary, 
                   usage.groupby('account_id')['usage_count'].sum().reset_index(), 
                   on='account_id', how='left')

# + Tickets (Service quality check)
summary = pd.merge(summary, 
                   tickets.groupby('account_id')['ticket_id'].count().reset_index().rename(columns={'ticket_id':'ticket_count'}), 
                   on='account_id', how='left')

# replace empty spaces with 0
summary = summary.fillna(0)

# 2. "Health Score"(Logic: More Usage + Less Tickets = Good Health)
summary['health_score'] = (summary['usage_count'] / 100) - (summary['ticket_count'] * 2)

print("\n--- 🏆 THE MASTER CUSTOMER DASHBOARD ---")
print(summary.sort_values(by='mrr_amount', ascending=False).head(10))

# Scatter Plot: Revenue vs Usage
plt.figure(figsize=(10, 6))
sns.scatterplot(data=summary, x='usage_count', y='mrr_amount', hue='plan_tier', size='ticket_count', sizes=(20, 200))
plt.title('Customer Value Map: Revenue vs Engagement')
plt.xlabel('Total Feature Usage')
plt.ylabel('Monthly Revenue ($)')
plt.show()

# Master Summary save for Power BI
summary.to_csv('data/powerbi_dashboard_data.csv', index=False)

# Funnel analysis stage-wise data
funnel_data = accounts['referral_source'].value_counts().reset_index()
funnel_data.to_csv('data/funnel_analysis.csv', index=False)