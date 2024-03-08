import unittest
from unittest.mock import MagicMock, call
from engine import execute_storyboard

class TestExecuteStoryboardComplex(unittest.TestCase):

    def test_story_branching_based_on_input(self):
        def snippet_branch(story_state):
            return ("Choose path: A or B?", 'input', lambda input: snippet_a if input == 'A' else snippet_b)

        def snippet_a(story_state):
            return ("Path A chosen", 'end', None)

        def snippet_b(story_state):
            return ("Path B chosen", 'end', None)

        # Correcting the mock setup and assertions
        get_input_mock = lambda: 'A'
        send_output_mock = MagicMock()

        story_state = []
        final_state_a = execute_storyboard(story_state, snippet_branch, get_input=get_input_mock, send_output=send_output_mock)

        # Correcting the assertion to match the expected structure
        self.assertTrue(any("Choose path: A or B?" in output for output in final_state_a[0]['texts']))
        send_output_mock.assert_any_call("Path A chosen")

    def test_story_accumulates_state_across_snippets(self):
        def snippet_accumulate(story_state):
            return ("Accumulate?", 'input', lambda input: snippet_accumulate_end)

        def snippet_accumulate_end(story_state):
            story_state.append("Accumulated")  # This appends directly to story_state
            return ("End", 'end', None)

        get_input_mock = lambda: 'yes'
        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_accumulate, get_input=get_input_mock, send_output=send_output_mock)
        
        # Correcting the assertion to accurately check for "Accumulated" in story_state
        # Since "Accumulated" is appended directly to story_state, we check the list directly
        self.assertIn("Accumulated", final_state)

        send_output_mock.assert_has_calls([call("Accumulate?"), call("End")])


    def test_story_repeats_snippet_on_invalid_input(self):
        def snippet_repeat(story_state):
            return ("Repeat on invalid. Valid: yes", 'input', lambda input: snippet_end if input == 'yes' else snippet_repeat)

        def snippet_end(story_state):
            return ("Valid input received", 'end', None)

        get_input_mock = MagicMock(side_effect=['no', 'yes'])
        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_repeat, get_input=get_input_mock, send_output=send_output_mock)
        
        expected_calls = [call("Repeat on invalid. Valid: yes"), call("Repeat on invalid. Valid: yes"), call("Valid input received")]
        send_output_mock.assert_has_calls(expected_calls)

    def test_story_handles_empty_input_correctly(self):
        """Test that the story can handle empty input and repeat the snippet."""
        def snippet_handle_empty_input(story_state):
            return ("Say 'continue' to proceed.", 'input', lambda input: snippet_success if input.strip().lower() == 'continue' else snippet_handle_empty_input)

        def snippet_success(story_state):
            return ("Successfully continued.", 'end', None)

        get_input_mock = MagicMock(side_effect=['', ' ', 'continue'])
        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_handle_empty_input, get_input=get_input_mock, send_output=send_output_mock)

        # Expect the snippet to be repeated until valid input ('continue') is received
        expected_calls = [call("Say 'continue' to proceed.") for _ in range(3)] + [call("Successfully continued.")]
        send_output_mock.assert_has_calls(expected_calls)

    def test_story_with_multiple_inputs_and_decisions(self):
        """Test a story that requires multiple inputs and makes several decisions based on those inputs."""
        def snippet_multiple_decisions(story_state):
            return ("First decision: 'left' or 'right'?", 'input', lambda input: snippet_second_decision if input == 'left' else snippet_end_fail)

        def snippet_second_decision(story_state):
            return ("Second decision: 'up' or 'down'?", 'input', lambda input: snippet_success if input == 'up' else snippet_end_fail)

        def snippet_success(story_state):
            return ("You've made it!", 'end', None)

        def snippet_end_fail(story_state):
            return ("Wrong choice. Game over.", 'end', None)

        get_input_mock = MagicMock(side_effect=['left', 'up'])
        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_multiple_decisions, get_input=get_input_mock, send_output=send_output_mock)

        # Verify the correct path through the story based on the inputs
        expected_calls = [call("First decision: 'left' or 'right'?"), call("Second decision: 'up' or 'down'?"), call("You've made it!")]
        send_output_mock.assert_has_calls(expected_calls)

    def test_story_ends_immediately(self):
        """Test a story snippet that ends the story immediately without input."""
        def snippet_end_immediately(story_state):
            return ("The end.", 'end', None)

        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_end_immediately, get_input=lambda: 'unused', send_output=send_output_mock)

        # Verify that the story ends immediately with the correct output
        send_output_mock.assert_called_once_with("The end.")

    def test_story_progresses_with_correct_input_after_incorrect_attempts(self):
        """Test that the story progresses correctly after one or more incorrect input attempts."""
        def snippet_retry_on_incorrect(story_state):
            return ("Correct answer is 'yes'.", 'input', lambda input: snippet_success if input == 'yes' else snippet_retry_on_incorrect)

        def snippet_success(story_state):
            return ("Correct answer received.", 'end', None)

        get_input_mock = MagicMock(side_effect=['no', 'maybe', 'yes'])
        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_retry_on_incorrect, get_input=get_input_mock, send_output=send_output_mock)

        # Verify the snippet is repeated until the correct input is received
        expected_calls = [call("Correct answer is 'yes'.") for _ in range(3)] + [call("Correct answer received.")]
        send_output_mock.assert_has_calls(expected_calls)

    def test_story_with_dynamic_decision_function(self):
        """Test a story snippet that dynamically decides the next snippet based on input."""
        def snippet_dynamic_decision(story_state):
            return ("Choose 'A' or 'B':", 'input', lambda input: snippet_a if input == 'A' else snippet_b)

        def snippet_a(story_state):
            return ("Option A chosen.", 'end', None)

        def snippet_b(story_state):
            return ("Option B chosen.", 'end', None)

        # First, test choosing option 'A'
        get_input_mock_a = lambda: 'A'
        send_output_mock_a = MagicMock()

        story_state_a = []
        final_state_a = execute_storyboard(story_state_a, snippet_dynamic_decision, get_input=get_input_mock_a, send_output=send_output_mock_a)

        send_output_mock_a.assert_has_calls([call("Choose 'A' or 'B':"), call("Option A chosen.")])

        # Then, test choosing option 'B'
        get_input_mock_b = lambda: 'B'
        send_output_mock_b = MagicMock()

        story_state_b = []
        final_state_b = execute_storyboard(story_state_b, snippet_dynamic_decision, get_input=get_input_mock_b, send_output=send_output_mock_b)

        send_output_mock_b.assert_has_calls([call("Choose 'A' or 'B':"), call("Option B chosen.")])


    def test_story_ends_with_no_output(self):
        """Test a story snippet that ends the story without any output."""
        def snippet_end_no_output(story_state):
            return ("", 'end', None)

        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_end_no_output, get_input=lambda: 'unused', send_output=send_output_mock)

        # Verify that the story ends without any output
        send_output_mock.assert_called_once_with("")

    def test_story_with_looping_snippets(self):
        """Test a story that loops back to a previous snippet based on user input."""
        def snippet_loop_start(story_state):
            return ("Loop start. Say 'loop' to loop, 'end' to end.", 'input', lambda input: snippet_loop_start if input == 'loop' else snippet_end)

        def snippet_end(story_state):
            return ("Loop ended.", 'end', None)

        get_input_mock = MagicMock(side_effect=['loop', 'loop', 'end'])
        send_output_mock = MagicMock()

        story_state = []
        final_state = execute_storyboard(story_state, snippet_loop_start, get_input=get_input_mock, send_output=send_output_mock)

        # Verify the story loops correctly and ends based on user input
        expected_loop_calls = [call("Loop start. Say 'loop' to loop, 'end' to end.") for _ in range(3)] + [call("Loop ended.")]
        send_output_mock.assert_has_calls(expected_loop_calls)

if __name__ == '__main__':
    unittest.main()

