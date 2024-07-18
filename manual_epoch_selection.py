from Recordings import Recordings, AEPFeedbackRecordings, AEPRecordings
import matplotlib
import matplotlib.pyplot as plt
import os
import mne

matplotlib.use('TkAgg')

if __name__ == '__main__':
    basepath = './Recordings'
    recordings = Recordings(basepath)
    aep_recordings = AEPRecordings(directory=None, recordings=recordings.filter_by(experiment_id='aep').recordings)
    aep_feedback_recordings = AEPFeedbackRecordings(directory=None, recordings=recordings.filter_by(
        experiment_id='aep_feedback').recordings)
    for recording in aep_recordings.recordings:
        recording.plot_epochs(scale_mV=50e-6)
        # plt.show()
        # At this point bad epochs are dropped, save the epochs to disk
        output_path = f"./Selected_Epochs/{recording.recording_name.replace('.xdf', '-epo.fif')}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        recording._epochs.save(output_path, overwrite=True)
    for aep_feedback_recording in aep_feedback_recordings.recordings:
        aep_feedback_recording.plot_epochs(scale_mV=50e-6)
        # plt.show()
        # At this point bad epochs are dropped, save the epochs to disk
        output_path = f"./Selected_Epochs/{aep_feedback_recording.recording_name.replace('.xdf', '-epo.fif')}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        aep_feedback_recording._epochs.save(output_path, overwrite=True)
