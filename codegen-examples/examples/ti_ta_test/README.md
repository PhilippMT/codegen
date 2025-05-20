# Ti Ta Test Example

This playful example demonstrates how to use the Codegen SDK to create a simple rhythm generator. It's a fun way to explore the capabilities of the Codegen SDK while creating something musical.

## What This Example Does

This example:

1. Initializes a Codegen Agent with your organization ID and API token
2. Runs the agent with a prompt to generate a rhythmic pattern based on "Ti Ta" syllables
3. Monitors the task status until completion
4. Displays the generated rhythm pattern
5. Optionally plays the rhythm if you have the required dependencies

## Usage

```bash
# Make sure you have the Codegen SDK installed
pip install codegen

# For audio playback (optional)
pip install simpleaudio

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
Running agent with prompt: "Generate a rhythmic pattern using Ti and Ta syllables"
Task status: running
Task status: running
Task status: completed
Generated Rhythm Pattern:
Ti-Ta-Ti-Ti Ta-Ta Ti-Ta-Ti-Ti Ta-Ta
Ti-Ti-Ta Ta-Ti-Ti Ta-Ta-Ta
```

If you have the `simpleaudio` package installed, the script will also play the rhythm using simple tones.

## Key Concepts

- **Creative Prompting**: Using the agent for creative tasks
- **Result Processing**: Parsing and using the agent's response
- **Optional Audio Output**: Extending the example with audio capabilities

This example shows how Codegen can be used for creative applications beyond code generation.