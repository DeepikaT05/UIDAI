import pandas as pd
import numpy as np
from pathlib import Path

# Paths
DATA_DIR = Path('data')
OUTPUT_DIR = Path('outputs/summary_tables')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_data():
    print("🚀 Starting Master Analysis...")

    # 1. Enrolment Analysis
    enrol_files = list((DATA_DIR / 'enrolment').glob('*.csv'))
    enrol_df = pd.concat([pd.read_csv(f) for f in enrol_files], ignore_index=True)
    enrol_df['state'] = enrol_df['state'].str.strip().str.title()
    enrol_df['total'] = enrol_df['age_0_5'] + enrol_df['age_5_17'] + enrol_df['age_18_greater']
    
    enrol_summary = enrol_df.groupby('state').agg({
        'total': 'sum',
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum'
    }).sort_values('total', ascending=False)
    
    enrol_summary.to_csv(OUTPUT_DIR / 'enrolment_state_summary.csv')
    print("✅ Enrolment summary generated.")

    # 2. Demographic Analysis
    demo_files = list((DATA_DIR / 'demographic').glob('*.csv'))
    demo_df = pd.concat([pd.read_csv(f) for f in demo_files], ignore_index=True)
    demo_df.columns = ['date', 'state', 'district', 'pincode', 'demo_age_5_17', 'demo_age_17_plus']
    demo_df['state'] = demo_df['state'].str.strip().str.title()
    demo_df['total_demo'] = demo_df['demo_age_5_17'] + demo_df['demo_age_17_plus']
    
    demo_summary = demo_df.groupby('state').agg({
        'total_demo': 'sum',
        'demo_age_5_17': 'sum',
        'demo_age_17_plus': 'sum'
    }).sort_values('total_demo', ascending=False)
    
    demo_summary.to_csv(OUTPUT_DIR / 'demographic_state_summary.csv')
    print("✅ Demographic summary generated.")

    # 3. Biometric Analysis
    bio_files = list((DATA_DIR / 'biometric').glob('*.csv'))
    bio_df = pd.concat([pd.read_csv(f) for f in bio_files], ignore_index=True)
    bio_df.columns = ['date', 'state', 'district', 'pincode', 'bio_age_5_17', 'bio_age_17_plus']
    bio_df['state'] = bio_df['state'].str.strip().str.title()
    bio_df['total_bio'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_plus']
    
    bio_summary = bio_df.groupby('state').agg({
        'total_bio': 'sum',
        'bio_age_5_17': 'sum',
        'bio_age_17_plus': 'sum'
    }).sort_values('total_bio', ascending=False)
    
    bio_summary.to_csv(OUTPUT_DIR / 'biometric_state_summary.csv')
    print("✅ Biometric summary generated.")

    # 4. Combined Lifecycle Report
    combined = enrol_summary.merge(demo_summary, on='state', how='outer')
    combined = combined.merge(bio_summary, on='state', how='outer').fillna(0)
    
    combined['system_load'] = combined['total'] + combined['total_demo'] + combined['total_bio']
    combined['priority_index'] = (
        (combined['system_load'] / combined['system_load'].max() * 40) +
        ((combined['age_0_5'] + combined['age_5_17']) / combined['total'].max() * 30) +
        ((combined['total_demo'] + combined['total_bio']) / (combined['total'] + 1) * 30)
    )
    
    # Identify Lifecycle Transaction Load Hotspots
    final_report = combined.sort_values('priority_index', ascending=False)
    final_report.to_csv(OUTPUT_DIR / 'final_lifecycle_report.csv')
    
    print("✅ Master Lifecycle Transaction Load Report generated.")
    print("\n🚀 ALL ANALYSIS COMPLETE! Check the 'outputs/summary_tables' folder.")

if __name__ == "__main__":
    process_data()
