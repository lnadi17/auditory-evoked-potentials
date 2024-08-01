from Recordings import Recordings, AEPFeedbackRecordings, AEPRecordings
import matplotlib
import json

matplotlib.use('TkAgg')

if __name__ == '__main__':
    basepath = './Recordings'
    recordings = Recordings(basepath)
    aep_recordings = AEPRecordings(directory=None, recordings=recordings.filter_by(experiment_id='aep').recordings)
    aep_feedback_recordings = AEPFeedbackRecordings(directory=None, recordings=recordings.filter_by(
        experiment_id='aep_feedback').recordings)

    selected_epochs = {}
    for recording in aep_recordings.recordings:
        recording.plot_epochs(scale_mV=50e-6)
        selected_epochs[recording.recording_name] = list(recording._epochs.selection)
    for aep_feedback_recording in aep_feedback_recordings.recordings:
        aep_feedback_recording.plot_epochs(scale_mV=50e-6)
        # https://mne.discourse.group/t/how-to-get-indices-for-dropped-epochs-from-a-subset-of-epochs/5901/5
        selection = list(aep_feedback_recording._epochs.selection)
        # Select indices where epochs are NOT ignored
        not_ignored_indices = [i for i, log in enumerate(aep_feedback_recording._epochs.drop_log)
                               if log != ('IGNORED',)]
        # Convert selection indices to indices of epochs that are not ignored
        selection = [not_ignored_indices.index(i) for i in selection]
        selected_epochs[aep_feedback_recording.recording_name] = selection

    # Write output to JSON file
    with open('manually_selected_epochs.json', 'w') as f:
        json.dump(selected_epochs, f, default=str)
