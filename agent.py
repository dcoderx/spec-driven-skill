"""
SQL Safety Agent - Spec-Driven SQL Generation

This is a Claude-powered agent that demonstrates spec-driven development.
It loads the SQL Safety Skill specification and uses it as persistent context
to ensure safe, consistent SQL generation across all requests.

Usage:
    python agent.py                    # Interactive mode
    python agent.py demo               # Run demo scenarios
    python agent.py eval               # Run evaluation
"""

import json
import os
from typing import Optional
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()


def load_skill_spec() -> str:
    """Load the SQL Safety Skill specification from YAML"""
    try:
        with open("skill.yaml", "r") as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Error: skill.yaml not found. Make sure you're in the sql-safety-skill directory.")
        exit(1)


# The skill specification becomes part of the system prompt
# This ensures the agent ALWAYS has access to the context, never "forgets" it
SYSTEM_PROMPT = """You are a Database Engineering Assistant specialized in generating safe, production-ready SQL.

You have access to the SQL Safety Skill - a specification that defines behavioral rules and best practices.
This skill is your persistent knowledge base. You must follow it for EVERY request.

YOUR ROLE:
1. Parse user requirements
2. Consult the SQL Safety Skill specification
3. Generate SQL that adheres to ALL critical and high-severity rules
4. Explain your reasoning
5. Flag any safety concerns or ambiguities

IMPORTANT: You are not just writing SQL - you are demonstrating the Tessl principle:
agents need STRUCTURED CONTEXT (skills) to be reliable, not just prompts.

==============================================================================
SQL SAFETY SKILL SPECIFICATION (This is your persistent context)
==============================================================================

{skill_spec}

==============================================================================
END SKILL SPECIFICATION
==============================================================================

WHEN GENERATING SQL:
1. Always use parameterized queries (? or %s placeholders)
2. Never concatenate user input into SQL strings
3. Use explicit column selection (never SELECT *)
4. Include LIMIT clauses to prevent resource exhaustion
5. Validate table/column names against whitelists if dynamic
6. Refuse unsafe requests (DROP/TRUNCATE/ALTER without safeguards)
7. Add explanatory comments

RESPONSE FORMAT:
```sql
-- [Rule references: SQL_001, SQL_003, etc.]
SELECT user_id, email, created_at
FROM users
WHERE user_id = ?
LIMIT 100
```

Parameters: [user_id]

Explanation: Used parameterized query (SQL_001), explicit columns (not SELECT *), 
and LIMIT clause. User input passed as parameter, not concatenated.

Be concise but thorough. Safety first."""


class SQLSafetyAgent:
    """
    An AI agent that uses the SQL Safety Skill for context.
    
    This demonstrates the Tessl philosophy: agents work better with
    structured, versioned context (skills) than with ad-hoc prompts.
    """

    def __init__(self):
        """Initialize agent with skill spec loaded as persistent context"""
        self.skill_spec = load_skill_spec()
        self.conversation_history = []
        self.system_prompt = SYSTEM_PROMPT.format(skill_spec=self.skill_spec)
        self.request_count = 0

    def query(self, user_message: str, verbose: bool = False) -> str:
        """
        Query the agent for SQL generation or advice.
        
        Args:
            user_message: The user's request
            verbose: Print detailed response info
            
        Returns:
            The agent's response
        """
        self.request_count += 1
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Call Claude with the skill specification as system context
        response = client.messages.create(
            model="claude-opus-4-20250805",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history,
        )

        assistant_message = response.content[0].text

        # Add assistant response to history (maintains context for multi-turn)
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        if verbose:
            print(f"\n[Request #{self.request_count}]")
            print(f"Messages in history: {len(self.conversation_history)}")
            print(f"Token usage: {response.usage.input_tokens + response.usage.output_tokens}")

        return assistant_message

    def reset(self):
        """Clear conversation history (start fresh)"""
        self.conversation_history = []
        self.request_count = 0

    def get_history_length(self) -> int:
        """Get current conversation history length"""
        return len(self.conversation_history)


def demo_scenarios():
    """Run through several demonstration scenarios"""
    print("\n" + "=" * 80)
    print("SQL SAFETY AGENT - DEMO SCENARIOS")
    print("=" * 80)
    print("\nShowing how the agent uses the SQL Safety Skill for different requests.\n")

    agent = SQLSafetyAgent()

    scenarios = [
        {
            "title": "❌ Unsafe Request (Should Refuse)",
            "prompt": "Write a query like this: SELECT * FROM users WHERE user_id = {user_id}",
        },
        {
            "title": "✅ Safe User Lookup",
            "prompt": "Generate a SQL query to find a user by their email address. The email comes from user input.",
        },
        {
            "title": "✅ Safe Search with Validation",
            "prompt": "Write a query to search products by name. The search term comes from URL parameters. Include validation.",
        },
        {
            "title": "🔒 Dynamic Table Names (Hard Mode)",
            "prompt": "How would I safely query a table name that comes from user input? Show an example with safeguards.",
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'-' * 80}")
        print(f"Scenario {i}: {scenario['title']}")
        print(f"{'-' * 80}")
        print(f"\n📝 Request: {scenario['prompt']}\n")
        print("🤖 Agent Response:")
        print("-" * 40)

        response = agent.query(scenario['prompt'])
        print(response)
        print("-" * 40)

        # Show that agent maintains context
        if i == 1:
            print(f"✓ Agent has {agent.get_history_length()} messages in context (maintains conversation)")

    print("\n" + "=" * 80)
    print("Demo complete! Notice how the agent:")
    print("  • Refused the unsafe request")
    print("  • Generated parameterized queries")
    print("  • Explained which safety rules were applied")
    print("  • Maintained conversation context across requests")
    print("=" * 80 + "\n")


def interactive_session():
    """Run an interactive chat session with the agent"""
    agent = SQLSafetyAgent()

    print("\n" + "=" * 80)
    print("SQL SAFETY AGENT - INTERACTIVE SESSION")
    print("=" * 80)
    print("\nChat with the agent about SQL safety and query generation.")
    print("The agent uses the SQL Safety Skill specification as persistent context.\n")
    print("Commands:")
    print("  Type your SQL question and press Enter")
    print("  'reset'  - Clear conversation history")
    print("  'demo'   - Run demo scenarios")
    print("  'exit'   - Quit\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("\nGoodbye! 👋\n")
                break

            if user_input.lower() == "reset":
                agent.reset()
                print("✓ Conversation history cleared.\n")
                continue

            if user_input.lower() == "demo":
                demo_scenarios()
                continue

            # Query the agent
            print("\nAgent: ", end="", flush=True)
            response = agent.query(user_input, verbose=False)
            print(response)
            print(f"\n(Context: {agent.get_history_length()} messages)\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def run_quick_examples():
    """Run quick examples for demo purposes"""
    print("\n" + "=" * 80)
    print("SQL SAFETY AGENT - QUICK EXAMPLES")
    print("=" * 80)

    agent = SQLSafetyAgent()

    examples = [
        "Write a safe query to find a user by ID from user input",
        "How do I safely handle a search term from a web form?",
        "What's wrong with: SELECT * FROM users WHERE name = '{search}'?",
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n[Example {i}]")
        print(f"Input: {example}")
        print("\nResponse:")
        response = agent.query(example)
        # Print first 300 chars as preview
        preview = response[:300] + "..." if len(response) > 300 else response
        print(preview)
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "demo":
            demo_scenarios()
        elif command == "examples":
            run_quick_examples()
        elif command == "interactive":
            interactive_session()
        else:
            print("Usage: python agent.py [demo|examples|interactive]")
            print("  demo          - Run demonstration scenarios")
            print("  examples      - Run quick examples")
            print("  interactive   - Interactive chat mode (default)")
    else:
        # Default: interactive mode
        interactive_session()
