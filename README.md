\# AI Coding Assistant \& Code Review Agent



A beginner-focused Python AI coding assistant that combines code analysis, runtime execution, AI-assisted review, beginner-friendly tutoring, targeted fixing, and verification.



\## Current Scope



The current implementation focuses on Python.



Java and multi-language support are planned for the major-project phase and are not part of the current Python MVP.



\## Core Workflow



User

↓

Python Code Editor

↓

API

↓

AST Parser + Flake8 + Docker Runtime

↓

Evidence Builder

↓

AI Review / Local Review Fallback

↓

Beginner Tutor

↓

Local Fixer

↓

Verification

↓

Final Feedback



\## Main Features



\- Python syntax analysis using AST

\- Static analysis using Flake8

\- Docker-isolated Python execution

\- Runtime error detection and parsing

\- Beginner-friendly explanations and hints

\- Gemini-based AI code review

\- Local review fallback when Gemini is unavailable

\- Targeted local code fixing

\- Verification of generated fixes

\- Editor navigation to reported issue lines

\- API input validation

\- Request-size protection

\- Restricted CORS

\- Environment-controlled Flask debug mode



\## Project Structure



```text

ai-coding-assistant/

├── apps/

│   ├── api/

│   │   └── main.py

│   └── dashboard/

├── src/

│   ├── analysis/

│   ├── fixer/

│   ├── parser/

│   ├── review/

│   ├── runtime/

│   ├── schemas/

│   ├── tutor/

│   └── verification/

├── tests/

│   └── integration/

├── .env.example

├── .gitignore

├── pyproject.toml

├── requirements.txt

└── README.md

