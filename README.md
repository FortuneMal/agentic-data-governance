Agentic Data Governance Engine 🕵️‍♂️
An autonomous, full-stack, multi-agent AI system designed to audit datasets for POPIA (South African privacy law) compliance, identify data quality issues, and autonomously execute remediation scripts.
🚀 The ArchitectureThis project moves beyond standard RAG or basic chatbots by employing Agentic Workflows. Specialized AI agents autonomously select tools, analyze data, collaborate to generate executive reports, and safely mutate data with human oversight.The Brain: Llama 3.3 (70B) served via Groq for ultra-low latency inference.The Orchestration: CrewAI for managing agent roles, delegation, and sequential task execution.The Persistence: Supabase PostgreSQL for permanent cloud logging of audit reports.The Frontend: A Next.js 14 "Mission Control" dashboard to visualize AI logs and dataset health in real-time.
✨ Enterprise FeaturesAuto-Remediation (Action-Oriented AI): The AI doesn't just give advice; it writes and executes its own Python/Pandas scripts to mask PII (e.g., XXX-XXX-XXXX) and impute missing data, saving the results to a clean CSV.Self-Healing Code Execution: If the AI writes a Python script with a syntax error, a custom try/except tool loop catches the trace, feeds it back to the LLM, and allows the AI to debug its own code autonomously.Human-in-the-Loop (HITL) Safety Protocol: Built for high-stakes compliance environments. The pipeline pauses mid-execution, requiring human authorization (or override instructions) before committing the final audit to the database.
🤖 The AI CrewChief Privacy Officer: Uses Regex/Pandas tools to scan raw CSVs specifically for South African ID numbers, emails, and phones, flagging POPIA risks.Data Quality Engineer: Analyzes the dataset schema for missing values (NaN) and structural integrity.Governance Communicator: Synthesizes the technical findings into an actionable executive summary.Data Remediation Engineer: Reads the summary, maps it to the dataset schema, and safely executes a local Pandas script to clean the data.
📂 Monorepo Structureagentic-data-governance/
 ├── backend/               # Python AI Engine
 │    ├── main.py           # CrewAI Orchestration & Supabase logic
 │    ├── tools.py          # Custom LLM tools (Pandas, Regex, Code Execution)
 │    ├── sample_data.csv   # Raw input dataset
 │    └── cleaned_data.csv  # AI-generated output dataset
 │
 ├── frontend/              # Next.js 14 Dashboard
 │    ├── src/app/          # React components and routing
 │    └── package.json      # Node dependencies
 │
 ├── .env                   # API Keys (Groq, Supabase)
 └── README.md
🛠️ Tech StackBackend: Python 3.10+, CrewAI, LiteLLM, Groq Cloud API, Pandas.Frontend: Next.js 14 (App Router), React, Tailwind CSS, Lucide Icons, React-Markdown.Database: Supabase (PostgreSQL), Supabase-js.
⚙️ How to Run1. Start the Backend AI EngineEnsure your .env file contains your GROQ_API_KEY, SUPABASE_URL, and SUPABASE_KEY.cd backend
# Activate your virtual environment
python main.py
(Note: The terminal will pause midway through execution to request your HITL approval. Press Enter to proceed or type feedback to alter the AI's findings).2. Start the Frontend DashboardOpen a second terminal window to boot up the Next.js UI.cd frontend
npm install
npm run dev
Navigate to http://localhost:3000 to view the Mission Control dashboard and read your real-time Supabase audit logs.
