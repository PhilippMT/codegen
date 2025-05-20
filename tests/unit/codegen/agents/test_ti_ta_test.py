"""
Unit tests for the Ti Ta Test example.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from codegen.agents.agent import Agent
from codegen_examples.examples.ti_ta_test.run import check_credentials, monitor_task, extract_rhythm_pattern, play_rhythm, run


class TestTiTaTestExample:
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
    def sample_result(self):
        """Sample result from the agent."""
        return {
            "output": """
            Here's a rhythmic pattern using Ti and Ta syllables:
            
            Ti-Ta-Ti-Ti Ta-Ta Ti-Ta-Ti-Ti Ta-Ta
            Ti-Ti-Ta Ta-Ti-Ti Ta-Ta-Ta
            
            You can clap this rhythm or use percussion instruments to play it.
            """
        }

    def test_extract_rhythm_pattern(self, sample_result):
        """Test extracting rhythm patterns from agent response."""
        patterns = extract_rhythm_pattern(sample_result)
        
        assert len(patterns) == 2
        assert "Ti-Ta-Ti-Ti Ta-Ta Ti-Ta-Ti-Ti Ta-Ta" in patterns
        assert "Ti-Ti-Ta Ta-Ti-Ti Ta-Ta-Ta" in patterns

    def test_extract_rhythm_pattern_empty(self):
        """Test extracting rhythm patterns from empty response."""
        patterns = extract_rhythm_pattern({})
        assert patterns == []
        
        patterns = extract_rhythm_pattern({"output": "No rhythm patterns here"})
        assert patterns == []

    def test_play_rhythm_import_error(self):
        """Test play_rhythm handles missing dependencies gracefully."""
        with patch("codegen_examples.examples.ti_ta_test.run.simpleaudio", None):
            with patch("builtins.print") as mock_print:
                play_rhythm(["Ti-Ta-Ti"])
                mock_print.assert_called_with("To play the rhythm, install simpleaudio: pip install simpleaudio")

    @patch("codegen_examples.examples.ti_ta_test.run.simpleaudio")
    def test_play_rhythm(self, mock_simpleaudio):
        """Test play_rhythm with mocked simpleaudio."""
        # Setup mock numpy and simpleaudio
        with patch("codegen_examples.examples.ti_ta_test.run.np") as mock_np:
            mock_np.linspace.return_value = [0, 0.1, 0.2]
            mock_np.sin.return_value = [0, 0.1, 0.2]
            mock_np.zeros.return_value = [0, 0]
            mock_np.append.return_value = [0, 0.1, 0.2]
            mock_np.int16 = int
            
            # Mock play_buffer
            mock_play_obj = MagicMock()
            mock_simpleaudio.play_buffer.return_value = mock_play_obj
            
            # Call play_rhythm
            play_rhythm(["Ti-Ta"])
            
            # Verify simpleaudio was called
            assert mock_simpleaudio.play_buffer.called
            assert mock_play_obj.wait_done.called

    def test_run_success(self, mock_env_vars, mock_agent, sample_result):
        """Test running the example with successful completion."""
        # Set up the mock status responses
        mock_agent.get_status.side_effect = [
            {"status": "running", "result": None},
            {"status": "completed", "result": sample_result}
        ]

        with patch("codegen_examples.examples.ti_ta_test.run.Agent", return_value=mock_agent):
            with patch("codegen_examples.examples.ti_ta_test.run.play_rhythm") as mock_play:
                result = run("Generate a rhythm")
        
        # Verify the agent was initialized and run with the correct prompt
        mock_agent.run.assert_called_once_with("Generate a rhythm")
        
        # Verify we got the expected result
        assert "patterns" in result
        assert len(result["patterns"]) == 2
        assert "raw_result" in result
        assert result["raw_result"] == sample_result

    def test_run_error(self, mock_env_vars):
        """Test handling of errors during execution."""
        with patch("codegen_examples.examples.ti_ta_test.run.Agent", side_effect=Exception("Test error")):
            result = run()
        
        assert result == {"error": "Test error"}