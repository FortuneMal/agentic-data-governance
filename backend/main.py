"""
Agentic Data Governance Engine - Core Orchestrator

This module initializes the CrewAI agents and coordinates the execution 
of data privacy and quality audits using the Groq API.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from supabase import create_client, Client

from tools import DataTools

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()

# Validate API Key
if not os.environ.get("GROQ_API_KEY"):
    logging.error("GROQ_API_KEY is not set. Please check your .env file.")
    sys.exit(1)

# ==========================================
# 1. INITIALIZE THE LLM
# ==========================================

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0
)

# ==========================================
# 2. WRAP PHASE 1 TOOLS
# ==========================================

@tool("POPIA Scanner")
def scan_pii_tool(file_path: str) -> str:
    """Scans a CSV file for South African Personally Identifiable Information (PII)."""
    return DataTools.check_pii(file_path)

@tool("Quality Scanner")
def scan_quality_tool(file_path: str) -> str:
    """Scans a CSV file and extracts missing values and data gaps."""
    return DataTools.get_data_stats(file_path)

@tool("Python Execution Tool")
def run_code_tool(code: str) -> str:
    """Executes Python code to clean datasets. Input must be raw Python code."""
    return DataTools.execute_pandas_code(code)

DATA_FILE = "sample_data.csv"

# ==========================================
# 3. DEFINE THE AGENTS 
# ==========================================

privacy_officer = Agent(
    role='Chief Privacy Officer (South Africa)',
    goal='Identify any POPIA compliance risks within datasets.',
    backstory=(
        'You are a strict data privacy expert specializing in South African law. '
        'You hunt down unprotected ID numbers, emails, and phone numbers to protect user privacy.'
    ),
    verbose=True,
    allow_delegation=False,
    tools=[scan_pii_tool],
    llm=llm
)

data_janitor = Agent(
    role='Senior Data Quality Engineer',
    goal='Assess datasets for missing values and structural integrity.',
    backstory=(
        'You are an analytical data engineer. You hate messy data. Your job is to find nulls, '
        'gaps, and broken schema so downstream machine learning models do not fail.'
    ),
    verbose=True,
    allow_delegation=False,
    tools=[scan_quality_tool],
    llm=llm
)

documentation_librarian = Agent(
    role='Data Governance Communicator',
    goal='Translate technical audits into clear, supportive documentation for stakeholders.',
    backstory=(
        'You are a highly organized communicator. You take complex compliance '
        'and quality audits and write clear, actionable summaries for the engineering team.'
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

remediation_engineer = Agent(
    role='Lead Data Remediation Engineer',
    goal='Write and execute Python code to fix data quality and privacy issues.',
    backstory=(
        'You are a brilliant Senior Python developer. You receive audit reports '
        'and write pandas code to clean CSV files. You always save the fixed '
        'data to a new file called `cleaned_sample_data.csv`. You mask PII (like ID numbers '
        'and phone numbers) by replacing them with "XXX-XXX-XXXX". You fill missing '
        'numerical values with 0 and missing text with "Unknown".'
    ),
    verbose=True,
    allow_delegation=False,
    tools=[run_code_tool], # This gives the agent the ability to run code
    llm=llm
)

# ==========================================
# 4. DEFINE THE TASKS 
# ==========================================

privacy_task = Task(
    description=f'Scan the dataset located at {DATA_FILE} for PII. List the exact columns that pose a POPIA risk.',
    expected_output='A bulleted list of columns containing potential PII and a brief explanation of why they are risky under POPIA.',
    agent=privacy_officer,
    human_input=False
)

quality_task = Task(
    description=f'Analyze the dataset located at {DATA_FILE} for missing values or quality issues.',
    expected_output='A clear breakdown of which columns have missing data and an overall assessment of the dataset health.',
    agent=data_janitor
)

reporting_task = Task(
    description='Review the findings from the Privacy Officer and Data Quality Engineer. Create a final executive summary.',
    expected_output='A professional markdown report detailing the dataset health, the privacy risks found, and actionable next steps.',
    agent=documentation_librarian,
    context=[privacy_task, quality_task] 
)

remediation_task = Task(
    description=(
        f'Read the final executive summary. Write and execute a Python pandas script '
        f'using your tool to clean {DATA_FILE} based on the findings. '
        f'CRITICAL: The summary might use descriptive names (like "email_address" or "phone_number"). '
        f'You must strictly map those to the actual CSV columns: user_id, email, sa_id, phone_number, age, purchase_amount. '
        f'Ignore any columns in the report that do not exist in this list. '
        f'Ensure the new file is saved as "cleaned_sample_data.csv".'
    ),
    expected_output='A confirmation message that the Python code ran successfully and the new file was created.',
    agent=remediation_engineer,
    context=[reporting_task] 
)

# ==========================================
# 5. ASSEMBLE AND RUN THE CREW
# ==========================================

governance_crew = Crew(
    agents=[privacy_officer, data_janitor, documentation_librarian, remediation_engineer],
    tasks=[privacy_task, quality_task, reporting_task, remediation_task],
    process=Process.sequential 
)

def main():
    """Main execution function for the Governance Engine."""
    logging.info("Starting the Agentic Data Governance Engine...")
    logging.info(f"Target Dataset: {DATA_FILE}")
    
    # Verify Supabase Keys exist
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        logging.error("Supabase credentials missing from .env file.")
        sys.exit(1)

    print("\n" + "="*50)
    print("INITIALIZING AUDIT WORKFLOW")
    print("="*50 + "\n")

    try:
        # 1. Kick off the agents
        result = governance_crew.kickoff()
        
        print("\n" + "="*50)
        print("FINAL GOVERNANCE REPORT")
        print("="*50 + "\n")
        # FIX: Explicitly grab the output from the reporting task
        print(reporting_task.output.raw) 
        
        # 2. Save to Supabase
        logging.info("Connecting to Supabase Cloud...")
        supabase: Client = create_client(url, key)
        
        # Insert the new report
        data, count = supabase.table('governance_reports').insert({
            "target_file": DATA_FILE, 
            "report_content": reporting_task.output.raw # FIX: Save the actual report
        }).execute()
        
        logging.info("Report permanently saved to Supabase!")
        
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()