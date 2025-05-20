#!/usr/bin/env python3
"""
Hello World Example for Codegen SDK

This example demonstrates the basic usage of the Codegen SDK by:
1. Initializing an Agent with credentials
2. Running a simple "Hello World" task
3. Monitoring the task status until completion
4. Displaying the result
"""

import os
import time
from typing import Dict, Any, Optional

import codegen
from codegen import Agent


def check_credentials() -> Dict[str, str]:
    """
    Check for required Codegen credentials in environment variables.
    
    Returns:
        Dict containing org_id and token if available
        
    Raises:
        ValueError: If required credentials are missing
    """
    org_id = os.environ.get("CODEGEN_ORG_ID")
    token = os.environ.get("CODEGEN_API_TOKEN")
    
    if not org_id:
        raise ValueError("CODEGEN_ORG_ID environment variable is required")
    if not token:
        raise ValueError("CODEGEN_API_TOKEN environment variable is required")
        
    return {"org_id": org_id, "token": token}


def monitor_task(agent: Agent, max_attempts: int = 10, delay: int = 2) -> Optional[Dict[str, Any]]:
    """
    Monitor a task until it completes or reaches max attempts.
    
    Args:
        agent: The Codegen Agent with an active task
        max_attempts: Maximum number of status checks
        delay: Seconds to wait between status checks
        
    Returns:
        Task result dictionary or None if task didn't complete
    """
    for _ in range(max_attempts):
        status = agent.get_status()
        if not status:
            print("No active task found")
            return None
            
        print(f"Task status: {status['status']}")
        
        if status["status"] == "completed":
            return status["result"]
        elif status["status"] == "failed":
            print(f"Task failed: {status.get('result', {}).get('error', 'Unknown error')}")
            return None
            
        time.sleep(delay)
    
    print(f"Task did not complete after {max_attempts} attempts")
    return None


@codegen.function("hello-world")
def run(prompt: str = "Hello World") -> Dict[str, Any]:
    """
    Run a simple Hello World example with the Codegen SDK.
    
    This function:
    1. Initializes a Codegen Agent with credentials
    2. Runs the agent with the provided prompt
    3. Monitors the task until completion
    4. Returns the task result
    
    Args:
        prompt: The prompt to send to the agent (default: "Hello World")
        
    Returns:
        Dictionary containing the task result
    """
    try:
        # Get credentials
        creds = check_credentials()
        
        print("Initializing Codegen Agent...")
        agent = Agent(
            org_id=creds["org_id"],
            token=creds["token"]
        )
        
        print(f"Running agent with prompt: \"{prompt}\"")
        task = agent.run(prompt)
        
        # Monitor task until completion
        result = monitor_task(agent)
        
        if result:
            print(f"Task result: {result}")
            return result
        
        return {"error": "Task did not complete successfully"}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    # For demonstration purposes, you can override the prompt here
    result = run("Hello World")