import pandas as pd
import re

class DataTools:
    @staticmethod
    def check_pii(file_path):
        """Scans the CSV for South African ID patterns."""
        df = pd.read_csv(file_path).astype(str) 
        id_pattern = r'\d{13}' 
        findings = []
        
        for col in df.columns:
            matches = df[col].apply(lambda x: bool(re.search(id_pattern, str(x))))
            if matches.any():
                findings.append(f"Potential PII detected in column: {col}")
                
        # Fix: Force the output to be a single string instead of a list
        if findings:
            return "\n".join(findings)
        else:
            return "No PII detected."

    @staticmethod
    def get_data_stats(file_path):
        """Returns missing value counts and basic stats."""
        df = pd.read_csv(file_path)
        null_counts = df.isnull().sum().to_dict()
        # Fix: Also wrap this output in a string conversion just to be safe
        return str(f"Missing values per column: {null_counts}")