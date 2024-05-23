from Recordings import Recordings
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cv2
import mne


# plt.ion()  # Enable interactive mode
def plot_subjects(recordings):
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
        fig = mne.viz.plot_compare_evokeds(evokeds, combine="mean", title=f'Subject {i}')[0]
        fig.savefig(f'./images/subject_{i}.png')

    if __name__ == '__main__':
        basepath = './Recordings'
        recordings = Recordings(basepath)
        # Get feedback recordings
        feedback_recordings = recordings.filter_by(experiment_id='aep_feedback')
        # sample.plot_epochs()
        # plt.show()
        # sample.plot_condition('standard')
        # sample.plot_condition('oddball')

        # for i, recording in enumerate(feedback_recordings):
        #     id = recording.subject_id
        #     recording.compare_conditions(save=True, name=f'feedback_{id}')

        plot_subjects(recordings)
