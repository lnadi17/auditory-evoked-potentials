import os
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
