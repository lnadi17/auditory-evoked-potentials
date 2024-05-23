import os

from Recording import Recording, AEPFeedbackRecording


class Recordings:
    def __init__(self, directory):
        self.recordings: [Recording] = []
        for path in self._get_all_file_paths(directory):
            print("Reading recording:", path)
            if path.endswith('.xdf'):
                if 'aep_feedback' in path:
                    self.recordings.append(AEPFeedbackRecording(path))
                else:
                    # TODO: Create a derived class for AEP recording
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
        return filtered_recordings

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
        for recording in self.filter_by(group, session, subject_id, experiment_id):
            recording.print_info()
