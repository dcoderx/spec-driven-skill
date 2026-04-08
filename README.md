# SQL Safety Skill

A **spec-driven, evaluated skill** for ensuring AI coding agents write secure SQL queries. Built to demonstrate the Tessl paradigm of structured context management for AI agents.

## What This Is

This is a reusable **skill package** for AI agents—a production-ready example of spec-driven development. Instead of asking an AI agent to "write safe SQL," we provide:

1. **Structured Specification** (`skill.yaml`) - Behavioral rules, constraints, and test scenarios
2. **Evaluation Framework** (`evaluator.py`) - Automated testing proving the agent actually follows the rules
3. **Versioning & Reusability** - Can be shared across projects, agents, and teams

This directly addresses the Tessl philosophy: **"Agents need structured context, not prompts."**

## The Problem This Solves

AI agents can write code, but they frequently make security mistakes:
- ❌ SQL injection vulnerabilities
- ❌ Forgotten input validation
- ❌ Unsafe string concatenation

Why? Because they lack **structured, versioned context** about what "safe SQL" means in your organization.

## The Solution: Spec-Driven Skills

Instead of hoping the agent remembers security rules, we encode them as:

```yaml
name: sql-safety-skill
version: 1.0.0
behavioral_rules:
  - rule_id: "SQL_001"
    name: "Parameterized Queries Required"
    severity: critical
```

Then we **evaluate** whether an agent follows it:

```
🧪 Running: TEST_001 - Basic parameterization
   ✅ PASS (Score: 95.00%)
```

## Quick Start

### 1. Install Dependencies

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

### 2. Run Evaluation

```bash
python evaluator.py --run-all
```

## Skill Specification

The skill defines 5 critical behavioral rules:

| Rule | Name | Severity |
|------|------|----------|
| SQL_001 | Parameterized Queries Required | ⚠️ CRITICAL |
| SQL_002 | No Raw String Concatenation | ⚠️ CRITICAL |
| SQL_003 | Use ORM When Possible | 🟠 HIGH |
| SQL_004 | Input Validation Before Query | 🟠 HIGH |
| SQL_005 | Escape Identifiers for Dynamic Names | 🟡 MEDIUM |

## Test Scenarios

5 test scenarios evaluate agent compliance:

- **TEST_001 (Easy)**: Basic parameterization
- **TEST_002 (Medium)**: SQL injection resistance
- **TEST_003 (Hard)**: Dynamic table names
- **TEST_004 (Medium)**: Reject unsafe patterns
- **TEST_005 (Hard)**: Validation + parameterization

## How This Aligns with Tessl

This skill demonstrates three key Tessl concepts:

### 1. **Structured Context** (Not Prompts)
Context is machine-readable YAML, not buried in text instructions.

### 2. **Evaluation** (Not Hope)
Automated tests prove agents follow the rules. You can measure compliance.

### 3. **Reusability** (Not Duplication)
Share this skill across teams, projects, and agents.

## Project Structure

```
sql-safety-skill/
├── skill.yaml           # Specification (rules, scenarios)
├── evaluator.py         # Python evaluation framework
├── context/             # Supporting documentation
│   └── examples/
├── README.md            # This file
├── requirements.txt     # Dependencies
└── .gitignore
```

## Why This Matters for Tessl

Tessl's mission: **"Agents need structured context to write reliable code."**

This project shows:

✅ **I understand the problem**: Agents without context make mistakes

✅ **I understand the solution**: Specs > Prompts

✅ **I can build it**: Here's a working skill with evaluation

## Latest Results

```
Total Tests: 5
Passed: 5/5 (100%)
Average Score: 96.4%
```

MIT
