# radio_mp3_test.py
This is a Python program that simulates the radio/MP3 player’s FSM and runs the test cases to verify the transitions, including the omitted pairs and the faulty behaviors.
Explanation of the Program and Test Strategy
Program Structure:
The RadioMP3Player class implements the FSM with states (Radio, MP3, Traffic) and stimuli (Next, MP3, Radio, Traffic Alert Start, Traffic Alert End).
It tracks the current state, radio station, MP3 song, and previous state/station/song for proper restoration.
Two flags (faulty_traffic_return and faulty_radio_return) simulate the faults for testing.
The run_tests function executes all 15 test cases, setting the initial state and applying the stimulus to verify the outcome.
Test Case Execution:
Test Cases 1–8: Achieve transition coverage by testing all defined transitions in the FSM.
Test Cases 9–15: Test omitted state-stimulus pairs, assuming the player remains in the current state.
Fault Testing: Test Case 8 is rerun with faulty_traffic_return=True to simulate the fault where the player returns to Radio instead of MP3. Test Case 5 is rerun with faulty_radio_return=True to simulate returning to a random radio station.
Output:
Each test case prints the initial state, stimulus, expected outcome, actual outcome, and pass/fail status.
The fault tests demonstrate the deviations from the specification, confirming that Test Case 8 detects the Traffic Alert End fault and Test Case 5 detects the random radio station fault.
Running the Program:
Save the code as radio_mp3_test.py and run it with Python to see the test results.
The output will show all test cases passing under normal conditions and failing when the faults are simulated, confirming the test strategy’s ability to detect the specified faults.
This approach ensures a systematic and comprehensive test strategy, achieving transition coverage, addressing omitted pairs, and verifying the faults as required.
