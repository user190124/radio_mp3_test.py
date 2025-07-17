class RadioMP3Player:
    def __init__(self):
        self.state = "Radio"  # Initial state
        self.radio_station = "Station 1"  # Current radio station
        self.mp3_song = "Song 1"  # Current MP3 song
        self.prev_state = None  # Store previous state for traffic alert
        self.prev_radio_station = "Station 1"  # Last tuned radio station
        self.prev_mp3_song = "Song 1"  # Last played MP3 song
        self.faulty_traffic_return = False  # Simulate fault in iii
        self.faulty_radio_return = False  # Simulate fault in iv

    def press_next(self):
        if self.state == "Radio":
            self.radio_station = "Station " + str(int(self.radio_station.split()[1]) + 1)
            return f"Radio: {self.radio_station}"
        elif self.state == "MP3":
            self.mp3_song = "Song " + str(int(self.mp3_song.split()[1]) + 1)
            return f"MP3: {self.mp3_song}"
        elif self.state == "Traffic":
            return f"Traffic: Broadcast (unchanged)"
        
    def press_mp3(self):
        if self.state == "Radio":
            self.prev_state = "Radio"
            self.prev_radio_station = self.radio_station
            self.state = "MP3"
            self.mp3_song = "Song 1"
            return f"MP3: {self.mp3_song}"
        elif self.state == "MP3":
            return f"MP3: {self.mp3_song} (unchanged)"
        elif self.state == "Traffic":
            return f"Traffic: Broadcast (unchanged)"
        
    def press_radio(self):
        if self.state == "MP3":
            self.prev_state = "MP3"
            self.prev_mp3_song = self.mp3_song
            self.state = "Radio"
            if self.faulty_radio_return:
                self.radio_station = "Station 3"  # Simulate fault: random station
                return f"Radio: {self.radio_station} (random, FAULT)"
            else:
                self.radio_station = self.prev_radio_station
                return f"Radio: {self.radio_station}"
        elif self.state == "Radio":
            return f"Radio: {self.radio_station} (unchanged)"
        elif self.state == "Traffic":
            return f"Traffic: Broadcast (unchanged)"
        
    def traffic_alert_start(self):
        if self.state in ["Radio", "MP3"]:
            self.prev_state = self.state
            self.prev_radio_station = self.radio_station
            self.prev_mp3_song = self.mp3_song
            self.state = "Traffic"
            return "Traffic: Broadcast"
        return f"{self.state}: Unchanged"
        
    def traffic_alert_end(self):
        if self.state == "Traffic":
            if self.faulty_traffic_return and self.prev_state == "MP3":
                self.state = "Radio"  # Simulate fault: return to Radio instead of MP3
                self.radio_station = self.prev_radio_station
                return f"Radio: {self.radio_station} (FAULT)"
            else:
                self.state = self.prev_state
                if self.state == "Radio":
                    self.radio_station = self.prev_radio_station
                    return f"Radio: {self.radio_station}"
                else:
                    self.mp3_song = self.prev_mp3_song
                    return f"MP3: {self.mp3_song}"
        return f"{self.state}: Unchanged"

def run_tests():
    test_cases = [
        # Transition Coverage (Test Cases 1–8)
        ("1", "Radio", "Next", "Radio: Station 2", "Radio → Radio (Next)"),
        ("2", "Radio", "MP3", "MP3: Song 1", "Radio → MP3 (MP3)"),
        ("3", "Radio", "Traffic Alert Start", "Traffic: Broadcast", "Radio → Traffic (Traffic Alert Start)"),
        ("4", "MP3", "Next", "MP3: Song 2", "MP3 → MP3 (Next)"),
        ("5", "MP3", "Radio", "Radio: Station 1", "MP3 → Radio (Radio)"),
        ("6", "MP3", "Traffic Alert Start", "Traffic: Broadcast", "MP3 → Traffic (Traffic Alert Start)"),
        ("7", "Traffic (prev Radio)", "Traffic Alert End", "Radio: Station 1", "Traffic → Radio (Traffic Alert End)"),
        ("8", "Traffic (prev MP3)", "Traffic Alert End", "MP3: Song 1", "Traffic → MP3 (Traffic Alert End)"),
        # Omitted State-Stimulus Pairs (Test Cases 9–15)
        ("9", "Radio", "Radio", "Radio: Station 1 (unchanged)", "Radio, Radio (ignored)"),
        ("10", "Radio", "Traffic Alert End", "Radio: Station 1 (unchanged)", "Radio, Traffic Alert End (ignored)"),
        ("11", "MP3", "MP3", "MP3: Song 1 (unchanged)", "MP3, MP3 (ignored)"),
        ("12", "MP3", "Traffic Alert End", "MP3: Song 1 (unchanged)", "MP3, Traffic Alert End (ignored)"),
        ("13", "Traffic (prev MP3)", "Next", "Traffic: Broadcast (unchanged)", "Traffic, Next (ignored)"),
        ("14", "Traffic (prev MP3)", "MP3", "Traffic: Broadcast (unchanged)", "Traffic, MP3 (ignored)"),
        ("15", "Traffic (prev MP3)", "Radio", "Traffic: Broadcast (unchanged)", "Traffic, Radio (ignored)")
    ]

    player = RadioMP3Player()
    print("Running tests without faults:")
    for test_id, init_state, stimulus, expected, description in test_cases:
        # Set initial state
        player.state = init_state.split()[0] if "prev" not in init_state else "Traffic"
        player.radio_station = "Station 1"
        player.mp3_song = "Song 1"
        player.prev_state = "MP3" if "prev MP3" in init_state else "Radio" if "prev Radio" in init_state else None
        player.prev_radio_station = "Station 1"
        player.prev_mp3_song = "Song 1"
        
        # Apply stimulus
        if stimulus == "Next":
            result = player.press_next()
        elif stimulus == "MP3":
            result = player.press_mp3()
        elif stimulus == "Radio":
            result = player.press_radio()
        elif stimulus == "Traffic Alert Start":
            result = player.traffic_alert_start()
        elif stimulus == "Traffic Alert End":
            result = player.traffic_alert_end()
            
        print(f"Test {test_id}: {description}")
        print(f"Initial: {init_state}, Stimulus: {stimulus}, Expected: {expected}, Got: {result}, "
              f"{'Pass' if result == expected else 'Fail'}")

    # Test fault in iii: Traffic Alert End returns to Radio instead of MP3
    print("\nRunning Test 8 with fault (Traffic Alert End → Radio instead of MP3):")
    player = RadioMP3Player()
    player.state = "MP3"
    player.mp3_song = "Song 1"
    player.prev_radio_station = "Station 1"
    player.traffic_alert_start()  # MP3 → Traffic
    player.faulty_traffic_return = True
    result = player.traffic_alert_end()
    expected = "MP3: Song 1"
    print(f"Test 8: Traffic → MP3 (Traffic Alert End)")
    print(f"Initial: Traffic (prev MP3), Stimulus: Traffic Alert End, Expected: {expected}, Got: {result}, "
          f"{'Pass' if result == expected else 'Fail'}")

    # Test fault in iv: Radio button returns to random station
    print("\nRunning Test 5 with fault (Radio button → random station):")
    player = RadioMP3Player()
    player.state = "MP3"
    player.mp3_song = "Song 1"
    player.prev_radio_station = "Station 1"
    player.faulty_radio_return = True
    result = player.press_radio()
    expected = "Radio: Station 1"
    print(f"Test 5: MP3 → Radio (Radio)")
    print(f"Initial: MP3, Stimulus: Radio, Expected: {expected}, Got: {result}, "
          f"{'Pass' if result == expected else 'Fail'}")

if __name__ == "__main__":
    run_tests()