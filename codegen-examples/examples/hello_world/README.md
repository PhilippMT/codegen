# Hello World Example

This simple example demonstrates how to use the Codegen SDK to create and run a basic agent task. It's a great starting point for beginners to understand the core functionality of the Codegen SDK.

## What This Example Does

This example:

1. Initializes a Codegen Agent with your organization ID and API token
2. Runs the agent with a "Hello World" prompt
3. Monitors the task status until completion
4. Displays the result

## Usage

```bash
# Make sure you have the Codegen SDK installed
pip install codegen

# Set your Codegen credentials as environment variables
export CODEGEN_ORG_ID="your_org_id"
export CODEGEN_API_TOKEN="your_api_token"

# Run the example
python run.py
```

## Expected Output

When run successfully, you should see output similar to:

```
Initializing Codegen Agent...
Running agent with prompt: "Hello World"
Task status: running
Task status: running
Task status: completed
Task result: {"output": "Hello World! I'm the Codegen AI assistant. How can I help you today?"}
```

## Key Concepts

- **Agent Initialization**: Creating an agent with your credentials
- **Task Execution**: Running the agent with a prompt
- **Status Monitoring**: Checking task status until completion
- **Result Handling**: Processing the completed task result

This example serves as a foundation for more complex Codegen SDK applications.