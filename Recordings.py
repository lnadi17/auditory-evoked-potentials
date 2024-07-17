import os

from Recording import Recording, AEPFeedbackRecording, AEPRecording


class Recordings:
    def __init__(self, directory=None, recordings=None):
        if recordings is not None:
            self.recordings = recordings
            return

        self.recordings: [Recording] = []
        for path in self._get_all_file_paths(directory):
            if path.endswith('.xdf'):
                print("Reading recording:", path)
                self.recordings.append(Recording(path))

    def filter_by(self, group='*', session='*', subject_id='*', experiment_id='*'):
        filtered_recordings = []
        for recording in self.recordings:
            if group != '*' and recording.group != group:
                continue
            if session != '*' and recording.session != session:
                continue
            if subject_id != '*' and recording.subject_id != subject_id:
                continue
            if experiment_id != '*' and recording.experiment_id != experiment_id:
                continue
            filtered_recordings.append(recording)
        return Recordings(directory=None, recordings=filtered_recordings)

    @staticmethod
    def _get_all_file_paths(directory, contains_str=None):
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if contains_str is not None:
                    if contains_str in filepath:
                        file_paths.append(filepath)
                else:
                    file_paths.append(filepath)
        return file_paths

    def print_info(self, group='*', session='*', subject_id='*', experiment_id='*'):
        for recording in self.filter_by(group, session, subject_id, experiment_id).recordings:
            recording.print_info()
