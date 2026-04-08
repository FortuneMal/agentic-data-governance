# Agentic Data Governance Engine 🕵️‍♂️

An autonomous, multi-agent AI system designed to audit datasets for POPIA (South African privacy law) compliance and data quality issues.

## 🚀 The Architecture
This project moves beyond standard RAG by employing "Agentic Workflows" where specialized AI agents autonomously select tools, analyze data, and collaborate to generate executive reports.

* **The Brain:** Llama 3.3 (70B) served via Groq for ultra-low latency inference.
* **The Orchestration:** CrewAI for managing agent roles, delegation, and sequential task execution.
* **The Tools:** Custom Python/Pandas functions acting as the "eyes" for the agents to scan for PII (Regex) and null values.
* **The Persistence:** Automated SQLite logging for long-term audit tracking.

## 🤖 The Crew
1. **Chief Privacy Officer:** Scans raw CSVs specifically for South African ID numbers and flags POPIA risks.
2. **Data Quality Engineer:** Analyzes the dataset schema for missing values and structural integrity.
3. **Governance Communicator:** Synthesizes the technical findings into an actionable executive summary.

## 🛠️ Tech Stack
* Python 3.10+
* CrewAI & LiteLLM
* Groq Cloud API
* Pandas & SQLite

## ☁️ Persistence Layer (Supabase)
The engine automatically logs all audit outcomes to a Supabase PostgreSQL database. This allows compliance officers to maintain a historical record of dataset health and POPIA risks over time.

* **Table Structure:** `governance_reports`
* **Fields Captured:** `id`, `audit_date`, `target_file`, `report_content`