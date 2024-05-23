import os
import mne
import numpy as np
import pyxdf


class Recording:
    recording_name: str
    group: int
    session: int
    subject_id: int
    experiment_id: str

    def __init__(self, xdf_path):
        self.xdf_path = xdf_path
        self._parse_xdf_path()
        self._read_xdf_data()
        self._read_metadata()
        self._read_eeg_data()
        self._read_marker_data()
        self._validate_data()

    def _validate_data(self):
        try:
            message = f"Recording {self.recording_name} does not match its metadata."
            assert self.metadata['subject']['id'] == self.subject_id, message
            assert self.metadata['subject']['group'] == self.group, message
            assert self.metadata['subject']['session'] == self.session, message
        except AssertionError as e:
            print("WARNING, data validation failed.", e)

    def _read_xdf_data(self):
        self._xdf_data = pyxdf.load_xdf(self.xdf_path)[0]

    def _read_metadata(self):
        # Read info of the first stream
        info = self._xdf_data[0]['info']
        self.metadata = {
            "effective_sample_rate": info['effective_srate'],
            "subject": {
                "id": int(info['desc'][0]['subject'][0]['id'][0]),
                "group": int(info['desc'][0]['subject'][0]['group'][0]),
                "session": int(info['desc'][0]['subject'][0]['session'][0])
            },
        }

    def _read_eeg_data(self):
        # Read data of the first stream
        self.eeg_time = self._xdf_data[0]['time_stamps']
        self._time_offset = min(self.eeg_time)
        self.eeg_time = self.eeg_time - self._time_offset
        self.eeg_data = self._xdf_data[0]['time_series'][:, :8]
        self.accelerometer_data = self._xdf_data[0]['time_series'][:, 8:11]
        self.gyroscope_data = self._xdf_data[0]['time_series'][:, 11:14]
        self.battery_level_data = self._xdf_data[0]['time_series'][:, 14]
        self.counter_data = self._xdf_data[0]['time_series'][:, 15]
        self.validation_indicator_data = self._xdf_data[0]['time_series'][:, 16]

    def _read_marker_data(self):
        # Read data of the second stream
        self.marker_time = self._xdf_data[1]['time_stamps']
        self.marker_time = self.marker_time - self._time_offset
        self.marker_data = [x[0] for x in self._xdf_data[1]['time_series']]
        self.markers = list(set(self.marker_data))

    def _parse_xdf_path(self):
        filename = os.path.basename(self.xdf_path)
        split_slash = self.xdf_path.split('/')
        self.recording_name = filename
        self.group = int(split_slash[2])
        self.session = int(split_slash[4])
        self.subject_id = int(split_slash[3])
        self.experiment_id = 'aep_feedback' if 'aep_feedback' in filename else 'aep'

    def print_info(self):
        print("---")
        print(f"Recording name: {self.recording_name}")
        print(f"Group: {self.group}")
        print(f"Session: {self.session}")
        print(f"Subject ID: {self.subject_id}")
        print(f"Experiment ID: {self.experiment_id}")
        print("Metadata:")
        print(self.metadata)
        print("---")


class AEPFeedbackRecording(Recording):
    def __init__(self, xdf_path):
        super().__init__(xdf_path)
        self._create_mne_raw_data(max_frequency=60)
        self._read_feedback_data()

    def _create_mne_raw_data(self, max_frequency):
        info = mne.create_info(ch_names=['Fz', 'C3', 'Cz', 'C4', 'Pz', 'PO7', 'Oz', 'PO8'], ch_types=['eeg'] * 8,
                               sfreq=250)
        raw = mne.io.RawArray([1e-6 * self.eeg_data[:, i] for i in range(8)], info)
        raw.notch_filter(freqs=[47, 50, 53])
        raw.filter(0.1, max_frequency)
        self._raw = raw
        self.eeg_data = np.transpose(raw.get_data())

    def _read_feedback_data(self):
        self.mne_events = []
        self.trials = []
        # Count the number of trials
        for i, event in enumerate(self.marker_data):
            if event == 'trial-begin':
                try:
                    assert self.marker_data[i + 1] in ['standard', 'oddball'], i
                    assert 'response-received' in self.marker_data[i + 2] or 'was-missed' in self.marker_data[i + 2], i
                    # Search for 'trial-end', watch out for errors
                    trial_end_index = None
                    for j, event2 in enumerate(self.marker_data[i + 3:]):
                        if 'error' in event2:
                            break
                        if event2 == 'trial-end':
                            trial_end_index = i + 3 + j
                            break
                    assert trial_end_index is not None, i
                    assert self.marker_data[trial_end_index] == 'trial-end', i
                    assert 'rt' in self.marker_data[trial_end_index - 1], i
                except AssertionError as e:
                    print(f"WARNING, data validation failed. Skipping trial...", e)
                    continue
            else:
                continue
            stimulus = self.marker_data[i + 1]
            if 'was-missed' in self.marker_data[i + 2]:
                response = None
                reaction_time = None
            else:
                if stimulus == 'standard' and 'arrow_down' in self.marker_data[i + 2]:
                    response = 'correct'
                elif stimulus == 'oddball' and 'arrow_up' in self.marker_data[i + 2]:
                    response = 'correct'
                else:
                    response = 'incorrect'
                reaction_time = int(self.marker_data[trial_end_index - 1].split('-')[1][:-2])
            begin_time = self.marker_time[i]
            stimulus_time = self.marker_time[i + 1]
            response_time = None if 'was-missed' in self.marker_data[i + 2] else self.marker_time[i + 2]
            end_time = self.marker_time[trial_end_index]

            eeg_start_index = np.argmax(self.eeg_time >= begin_time)
            eeg_stimulus_index = np.argmax(self.eeg_time >= stimulus_time)
            eeg_response_index = np.argmax(self.eeg_time >= response_time) if response_time is not None else None
            eeg_end_index = np.argmax(self.eeg_time >= end_time)

            try:
                assert eeg_stimulus_index < eeg_end_index, f"Stimulus index is greater than end index. {i}"
                # Avoid overlapping events
                if self.mne_events and eeg_stimulus_index == self.mne_events[-1][0]:
                    eeg_stimulus_index += 1
                self.mne_events.append([eeg_stimulus_index, 0, 2 if stimulus == 'oddball' else 1])
                if response_time is not None:
                    # Avoid overlapping events
                    if eeg_response_index == self.mne_events[-1][0]:
                        eeg_response_index += 1
                    self.mne_events.append([eeg_response_index, 0, 3 if response == 'correct' else 4])
            except AssertionError as e:
                print(f"WARNING, data validation failed. Skipping trial...", e)

            self.trials.append({
                'time': self.eeg_time[eeg_start_index:eeg_end_index],
                'data': self.eeg_data[eeg_start_index:eeg_end_index],
                'stimulus': (eeg_stimulus_index, stimulus),  # TODO: Subtract eeg_start_index
                'reaction_time': reaction_time,
                'response': (eeg_response_index, response)  # TODO: Subtract eeg_start_index
            })
        self.mne_events = np.array(self.mne_events)
        event_dict = {'standard': 1, 'oddball': 2, 'correct': 3, 'incorrect': 4}
        self._epochs = mne.Epochs(self._raw, self.mne_events, event_id=event_dict, tmin=-0.2, tmax=0.8, preload=True,
                                  on_missing='ignore')
