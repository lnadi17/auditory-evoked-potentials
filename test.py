from Recordings import Recordings, AEPFeedbackRecordings, AEPRecordings
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
import mne


# plt.ion()  # Enable interactive mode
def plot_subjects_feedback(recordings):
    for i in range(1, 8):
        subject_recording = recordings.filter_by(experiment_id='aep_feedback', subject_id=i)
        # Merge epochs of all recordings of the same subject
        epochs = []
        for recording in subject_recording:
            epochs.append(recording._epochs)
        epochs = mne.concatenate_epochs(epochs)
        evokeds = dict(
            standard=list(epochs["standard"].iter_evoked()),
            oddball=list(epochs["oddball"].iter_evoked()),
        )
        fig = mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=['Cz'], title=f'Subject {i}')[0]
        fig.savefig(f'./images/Cz_{i}.png')


def plot_subjects(recordings):
    for i in range(1, 8):
        subject_recording = recordings.filter_by(experiment_id='aep', subject_id=i)
        # Merge epochs of all recordings of the same subject
        epochs = []
        for recording in subject_recording:
            epochs.append(recording._epochs)
        epochs = mne.concatenate_epochs(epochs)
        evokeds = dict(
            standard=list(epochs["standard"].iter_evoked()),
            oddball=list(epochs["oddball"].iter_evoked()),
        )
        fig = mne.viz.plot_compare_evokeds(evokeds, combine="mean", title=f'Subject {i}')[0]
        fig.savefig(f'./images/exp1_nobase_{i}.png')


if __name__ == '__main__':
    basepath = './Recordings'
    recordings = Recordings(basepath)
    # aep_recordings = AEPRecordings(directory=None, recordings=recordings.filter_by(experiment_id='aep').recordings)
