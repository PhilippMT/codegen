#!/usr/bin/env python3
"""
Ti Ta Test Example for Codegen SDK

This example demonstrates a creative use of the Codegen SDK by:
1. Initializing an Agent with credentials
2. Running a task to generate a rhythmic pattern using "Ti" and "Ta" syllables
3. Monitoring the task status until completion
4. Displaying and optionally playing the generated rhythm
"""

import os
import re
import time
from typing import Dict, Any, Optional, List

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


def extract_rhythm_pattern(result: Dict[str, Any]) -> List[str]:
    """
    Extract rhythm patterns from the agent's response.
    
    Args:
        result: The result dictionary from the agent
        
    Returns:
        List of rhythm pattern strings
    """
    if not result or "output" not in result:
        return []
    
    output = result["output"]
    
    # Look for patterns of Ti and Ta
    patterns = []
    
    # Find lines with Ti and Ta patterns
    for line in output.split("\n"):
        # Only include lines with Ti and Ta
        if re.search(r'\b(Ti|Ta)\b', line, re.IGNORECASE):
            # Clean up the line
            cleaned = re.sub(r'[^TitaA\-\s]', '', line)
            if cleaned.strip():
                patterns.append(cleaned.strip())
    
    return patterns


def play_rhythm(patterns: List[str]) -> None:
    """
    Play the rhythm pattern using simple audio tones.
    
    Args:
        patterns: List of rhythm pattern strings
    """
    try:
        import simpleaudio as sa
        import numpy as np
        
        print("Playing rhythm...")
        
        # Audio parameters
        sample_rate = 44100
        ti_freq = 880  # A5
        ta_freq = 440  # A4
        duration = 0.3  # seconds
        
        def get_tone(freq, duration):
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            tone = np.sin(freq * t * 2 * np.pi)
            # Apply fade in/out
            fade = 0.05
            fade_samples = int(fade * sample_rate)
            tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
            tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            # Normalize
            tone = (tone * 0.3 * 32767).astype(np.int16)
            return tone
        
        # Generate tones
        ti_tone = get_tone(ti_freq, duration)
        ta_tone = get_tone(ta_freq, duration)
        pause_tone = np.zeros(int(0.1 * sample_rate), dtype=np.int16)
        
        # Play each pattern
        for pattern in patterns:
            audio = np.array([], dtype=np.int16)
            
            # Convert pattern to audio
            for syllable in re.finditer(r'(Ti|Ta)', pattern, re.IGNORECASE):
                if syllable.group().lower() == 'ti':
                    audio = np.append(audio, ti_tone)
                else:  # Ta
                    audio = np.append(audio, ta_tone)
                audio = np.append(audio, pause_tone)
            
            # Play the pattern
            play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
            play_obj.wait_done()
            time.sleep(0.5)  # Pause between patterns
            
    except ImportError:
        print("To play the rhythm, install simpleaudio: pip install simpleaudio")


@codegen.function("ti-ta-test")
def run(prompt: str = "Generate a rhythmic pattern using Ti and Ta syllables") -> Dict[str, Any]:
    """
    Run the Ti Ta Test example with the Codegen SDK.
    
    This function:
    1. Initializes a Codegen Agent with credentials
    2. Runs the agent with a prompt to generate a rhythmic pattern
    3. Monitors the task until completion
    4. Extracts and returns the rhythm patterns
    
    Args:
        prompt: The prompt to send to the agent
        
    Returns:
        Dictionary containing the rhythm patterns and raw result
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
        
        if not result:
            return {"error": "Task did not complete successfully"}
        
        # Extract rhythm patterns
        patterns = extract_rhythm_pattern(result)
        
        if patterns:
            print("Generated Rhythm Pattern:")
            for pattern in patterns:
                print(pattern)
            
            # Try to play the rhythm
            play_rhythm(patterns)
        else:
            print("No rhythm patterns found in the response")
        
        return {
            "patterns": patterns,
            "raw_result": result
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Run the example
    result = run()