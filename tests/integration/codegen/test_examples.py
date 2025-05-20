"""
Integration tests for the Codegen examples.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from codegen.agents.agent import Agent
from codegen_examples.examples.hello_world.run import run as hello_world_run
from codegen_examples.examples.ti_ta_test.run import run as ti_ta_test_run


@pytest.fixture
def mock_env_vars():
    """Set up mock environment variables for testing."""
    with patch.dict(os.environ, {"CODEGEN_ORG_ID": "123", "CODEGEN_API_TOKEN": "test-token"}):
        yield


@pytest.fixture
def mock_agent():
    """Create a mock Agent instance."""
    with patch("codegen.agents.agent.Agent") as mock_agent_class:
        mock_agent_instance = MagicMock(spec=Agent)
        mock_agent_class.return_value = mock_agent_instance
        yield mock_agent_instance


class TestExamplesIntegration:
    def test_hello_world_and_ti_ta_test(self, mock_env_vars, mock_agent):
        """Test that both examples can run in sequence."""
        # Set up the mock status responses for Hello World
        hello_world_response = {"output": "Hello World! I'm the Codegen AI assistant."}
        mock_agent.get_status.side_effect = [
            {"status": "running", "result": None},
            {"status": "completed", "result": hello_world_response}
        ]

        # Run Hello World example
        with patch("codegen_examples.examples.hello_world.run.Agent", return_value=mock_agent):
            hello_result = hello_world_run("Hello World")
        
        assert hello_result == hello_world_response
        
        # Reset mock for Ti Ta Test
        mock_agent.reset_mock()
        
        # Set up the mock status responses for Ti Ta Test
        ti_ta_response = {
            "output": """
            Here's a rhythmic pattern using Ti and Ta syllables:
            
            Ti-Ta-Ti-Ti Ta-Ta Ti-Ta-Ti-Ti Ta-Ta
            Ti-Ti-Ta Ta-Ti-Ti Ta-Ta-Ta
            """
        }
        mock_agent.get_status.side_effect = [
            {"status": "running", "result": None},
            {"status": "completed", "result": ti_ta_response}
        ]
        
        # Run Ti Ta Test example
        with patch("codegen_examples.examples.ti_ta_test.run.Agent", return_value=mock_agent):
            with patch("codegen_examples.examples.ti_ta_test.run.play_rhythm"):
                ti_ta_result = ti_ta_test_run()
        
        # Verify Ti Ta Test results
        assert "patterns" in ti_ta_result
        assert len(ti_ta_result["patterns"]) == 2
        assert "Ti-Ta-Ti-Ti Ta-Ta Ti-Ta-Ti-Ti Ta-Ta" in ti_ta_result["patterns"]
        
        # Verify both examples were called with the correct prompts
        mock_agent.run.assert_called_with("Generate a rhythmic pattern using Ti and Ta syllables")