# Quick Start Guide - SQL Safety Skill

Get this running in 2 minutes.

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Set Your API Key
```bash
export ANTHROPIC_API_KEY=sk-...
```

## 3. Explore the Skill
```bash
cat skill.yaml
```

See the rules, conventions, and context that agents will use.

## 4. Run the Evaluator
```bash
python evaluator.py
```

This shows all 5 test cases that verify agent behavior.

## 5. Chat with the Agent (Interactive)
```bash
python agent.py
```

Example prompts:
- "Write a query to get all users created in the last 30 days"
- "How would you fetch payment records for a specific customer?"
- "What query would you write to delete spam entries?"

The agent will:
1. Generate safe SQL
2. Explain which safety rules it applied
3. List parameters separately
4. Flag any concerns

## 6. Run Full Evaluation (Demo)
```bash
python agent.py eval
```

This runs the agent through all 5 test scenarios and shows:
- Pass/fail for each test
- Overall pass rate
- Detailed results saved to `evaluation_results.json`

---

## For Your Interview Tomorrow

### 30-Second Pitch
"This is a spec-driven SQL safety skill. Instead of asking an AI agent 'write safe SQL' each time, I created a specification that codifies security rules, provides context, and includes tests to verify the agent follows them. This is exactly what Tessl does—but for any type of skill."

### Show These Files
1. **skill.yaml** - Shows you understand specs, versioning, rules
2. **evaluator.py** - Shows you understand testing/evaluation
3. **agent.py** - Shows a working example

### Run This Command
```bash
python agent.py eval
```

Watch as the agent gets evaluated against the rules you defined.

---

## What Makes This Tessl-Relevant

| Concept | This Project |
|---------|-------------|
| Specification | skill.yaml defines behavior before code |
| Versioning | Version 1.0.0, ready to be bumped to 1.1.0 |
| Context | Rules, conventions, examples = agent context |
| Evaluation | Tests prove agent behavior matches spec |
| Reusability | Any team could use this skill |
| Distribution | Ready for skill registry (Tessl Registry) |

---

## Next Steps

- **Extend**: Add more rules (performance, indexing, etc.)
- **Distribute**: Push to GitHub, reference in Tessl Registry
- **Scale**: Create skills for other domains (API design, code review, etc.)
- **Integrate**: Connect to real database to evaluate against actual schemas

---

Questions? Everything is spec-driven, tested, and versioned. That's the Tessl way.
