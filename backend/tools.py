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

    @staticmethod
    def execute_pandas_code(code_string):
        """Executes a Python script to manipulate data."""
        try:
            # LLMs love to wrap code in markdown blocks. This strips them out safely.
            clean_code = code_string.replace('```python', '').replace('```', '').strip()
            
            # Execute the code in an isolated local environment
            local_vars = {}
            exec(clean_code, globals(), local_vars)
            
            return "Success! The code executed and the data was cleaned."
        except Exception as e:
            # If the LLM writes bad code, this feeds the error back to it so it can try again
            return f"Execution Failed with error: {e}. Please rewrite the code and try again."