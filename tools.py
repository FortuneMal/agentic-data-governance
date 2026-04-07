import pandas as pd
import re

class DataTools:
    @staticmethod
    def check_pii(file_path):
        """Scans the CSV for South African ID patterns."""
        df = pd.read_csv(file_path)
        id_pattern = r'\d{13}' # Simple regex for 13-digit SA ID
        findings = []
        
        for col in df.columns:
            matches = df[col].astype(str).apply(lambda x: bool(re.search(id_pattern, x)))
            if matches.any():
                findings.append(f"Potential PII detected in column: {col}")
        return findings if findings else "No PII detected."

    @staticmethod
    def get_data_stats(file_path):
        """Returns missing value counts and basic stats."""
        df = pd.read_csv(file_path)
        null_counts = df.isnull().sum().to_dict()
        return f"Missing values per column: {null_counts}"