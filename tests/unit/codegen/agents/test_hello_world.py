"""
Unit tests for the Hello World example.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from codegen_api_client.models.agent_run_response import AgentRunResponse

from codegen.agents.agent import Agent, AgentTask
from codegen_examples.examples.hello_world.run import check_credentials, monitor_task, run


class TestHelloWorldExample:
    @pytest.fixture
    def mock_env_vars(self):
        """Set up mock environment variables for testing."""
        with patch.dict(os.environ, {"CODEGEN_ORG_ID": "123", "CODEGEN_API_TOKEN": "test-token"}):
            yield

    @pytest.fixture
    def mock_agent(self):
        """Create a mock Agent instance."""
        with patch("codegen.agents.agent.Agent") as mock_agent_class:
            mock_agent_instance = MagicMock(spec=Agent)
            mock_agent_class.return_value = mock_agent_instance
            yield mock_agent_instance

    @pytest.fixture
    def mock_task(self):
        """Create a mock AgentTask instance."""
        mock_task = MagicMock(spec=AgentTask)
        mock_task.id = "123"
        mock_task.status = "running"
        mock_task.result = None
        return mock_task

    def test_check_credentials(self, mock_env_vars):
        """Test that credentials are correctly retrieved from environment variables."""
        creds = check_credentials()
        assert creds["org_id"] == "123"
        assert creds["token"] == "test-token"

    def test_check_credentials_missing(self):
        """Test that an error is raised when credentials are missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="CODEGEN_ORG_ID environment variable is required"):
                check_credentials()

        with patch.dict(os.environ, {"CODEGEN_ORG_ID": "123"}, clear=True):
            with pytest.raises(ValueError, match="CODEGEN_API_TOKEN environment variable is required"):
                check_credentials()

    def test_monitor_task_completed(self, mock_agent):
        """Test monitoring a task that completes successfully."""
        # Set up mock status responses
        mock_agent.get_status.side_effect = [
            {"status": "running", "result": None},
            {"status": "completed", "result": {"output": "Hello World response"}}
        ]

        result = monitor_task(mock_agent, max_attempts=5, delay=0)
        
        assert result == {"output": "Hello World response"}
        assert mock_agent.get_status.call_count == 2

    def test_monitor_task_failed(self, mock_agent):
        """Test monitoring a task that fails."""
        mock_agent.get_status.return_value = {"status": "failed", "result": {"error": "Task failed"}}

        result = monitor_task(mock_agent, max_attempts=5, delay=0)
        
        assert result is None
        assert mock_agent.get_status.call_count == 1

    def test_monitor_task_timeout(self, mock_agent):
        """Test monitoring a task that times out."""
        # Always return running status
        mock_agent.get_status.return_value = {"status": "running", "result": None}

        result = monitor_task(mock_agent, max_attempts=3, delay=0)
        
        assert result is None
        assert mock_agent.get_status.call_count == 3

    def test_run_success(self, mock_env_vars, mock_agent, mock_task):
        """Test running the example with successful completion."""
        # Set up the mock agent to return our mock task
        mock_agent.run.return_value = mock_task
        
        # Set up the mock status responses
        mock_agent.get_status.side_effect = [
            {"status": "running", "result": None},
            {"status": "completed", "result": {"output": "Hello World response"}}
        ]

        with patch("codegen_examples.examples.hello_world.run.Agent", return_value=mock_agent):
            result = run("Test prompt")
        
        # Verify the agent was initialized and run with the correct prompt
        mock_agent.run.assert_called_once_with("Test prompt")
        
        # Verify we got the expected result
        assert result == {"output": "Hello World response"}

    def test_run_error(self, mock_env_vars):
        """Test handling of errors during execution."""
        with patch("codegen_examples.examples.hello_world.run.Agent", side_effect=Exception("Test error")):
            result = run("Test prompt")
        
        assert result == {"error": "Test error"}