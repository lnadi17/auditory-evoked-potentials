# Auditory Evoked Potentials

Check out the [project report](./Report.pdf) in Georgian language.

# Data Description

## Introduction

This dataset comprises EEG recordings from 10 volunteers who participated in two auditory oddball paradigm experiments. In the first experiment, subjects engaged in a passive listening task. The second experiment required active feedback from subjects via a keyboard, with their reaction times recorded. Each subject also underwent resting-state experiments with both eyes open and closed. Additionally, subjects completed a health information questionnaire, which is included with the data.

The EEG recordings were conducted using the Unicorn Hybrid Black device, capturing data from 8 EEG channels, as well as accelerometer and gyroscope readings from the headset. The recorded signals have a 24-bit resolution and a sampling rate of 250 Hz. Electrodes were positioned according to the international 10-20 system at the following sites: Fz, C3, Cz, C4, Pz, PO7, Oz, and PO8. All recordings were made under dry electrode conditions.

The experiments were designed and recorded using the NeuroPype™ Suite. The Unicorn LSL Interface was used for streaming headset data, while event markers were captured with the NeuroPype™ Experiment Recorder. Subsequent data processing was performed using the Python MNE library. The resulting data files are available in CSV format.

Given dataset is multipurpose and can be used to study phenomena ranging from simple resting-state analysis to Auditory Evoked Potentials (AEPs), as well as correlating EEG signals with reaction times and subjects' questionnaire responses. A detailed explanation of the experiments can be found below.

## Methods

Experiments took place in the Muskhelishvili Institute of Computational Mathematics (MICM). 10 participants were recruited (7 males, 3 females) aged 25 to 79 years. All participants were required to read and sign the consent document before conducting the experiment and providing their health information. To ensure privacy, each participant was assigned a unique subject ID (1 to 10). Participants completed two 20-minute recording sessions, each consisting of two AEP experiments. Subjects could have a break for as long as they wanted between the sessions. Resting-state responses were recorded either before or after the sessions. During the experiments, participants were instructed to sit comfortably, remain still, focus on a cross on the screen, and avoid any voluntary movements.

In experiment 1, subjects listened to 200 auditory stimuli train of 1000 Hz (standard) and 2000 Hz (oddball) pure tones, with an inter-stimulus time of 1.3 seconds. Both presented tones had a 100 ms duration. Standard tones were presented 80% of the time, while oddball tones appeared 20% of the time. The order of presented stimuli was pseudo-randomly generated, while also adhering to the rule that two oddball stimuli could not be played together. 200 trials were presented in 5 blocks, each consisting of 40 trials. Subjects could rest between the trial blocks. Also, they had to report the number of times they heard the oddball tone during that block, which was to ensure they were engaged in the task. 

In experiment 2, subjects again listened to 200 auditory stimuli with the same frequencies, proportions, and resting times as in experiment 1. The inter-stimulus time was 1.2 seconds. This time, subjects were instructed to give immediate feedback on a keyboard when they heard the stimulus (down arrow for standard, up arrow for oddball) while also trying to remain accurate. The responses of subjects and their reaction times were recorded along with the EEG data.

Resting-state experiments were conducted in two conditions, eyes open and eyes closed. Both of these conditions were recorded for 2 minutes. Subjects were instructed to remain as still as possible, maintain a relaxed state during the recordings, and avoid any specific thoughts or mental tasks during this period.

## File Structure

Each CSV file recording has 19 columns. Each column corresponds to an output channel acquired from the Unicorn Hybrid Black EEG device. There are different types of channels in the raw recording files: 1 time channel, 8 EEG channels, 3 accelerometer channels, 3 gyroscope channels, 1 counter channel, 1 validation channel, and 1 event channel.   
  
Specifically, all the 19 channels are: Time, EEG_Fz, EEG_C3, EEG_Cz, EEG_C4, EEG_Pz, EEG_PO7, EEG_Oz, EEG_PO8, Accelerometer_X, Accelerometer_Y, Accelerometer_Z, Gyroscope_X, Gyroscope_Y, Gyroscope_Z, Battery_Level, Counter, Validation, Event.  
  
1. *Time* column indicates a number of seconds passed since the start of the session.  
2. *EEG_\** columns indicate voltage values (in microvolts) for 8 EEG channels specified in the Unicord Hybrid Black EEG device manual. For each EEG channel an electrode position is indicated (e.g. Cz) according to the international 10-20 system.  
3. *Accelerometer_\** columns indicate acceleration (±8 g) of the Unicorn Hybrid Black EEG device in X/Y/Z directions.  
4. *Gyroscope_\** columns indicate the angular rotation (±1000 °/s) of Unicorn Hybrid Black EEG device in X/Y/Z directions.  
5. *Battery_Level* column value ranges from 0 to 100 and indicates the remaining battery level.  
6. *Counter* column tracks the sample order in which the values were received from Unicorn Hybrid Black to the host PC.  
7. *Validation* column is a validation indicator for the samples received from the Unicorn Hybrid Black device.  
8. *Event* column indicates if any event was registered during the recording. Event descriptions for different experiment types can be found below.  
  
More information about channels can be found in [Unicorn Hybrid Black User Manual](https://github.com/unicorn-bi/Unicorn-Suite-Hybrid-Black-User-Manual).  
  
**Note:** The data was streamed using the Unicorn LSL interface, which by itself outputs 17 raw channels (except "Time" and "Events" channels). Given channels were captured and exported into CSV files. Event markers were streamed (also using LSL protocol) by NeuroPype™ Experiment Recorder (ER) software. Both of these streams were exported in XDF file format and then automatically synced using the PyXDF library. As a result, the "Time" and "Events" columns were added to the CSV files.

## Event Descriptions

There are multiple event markers that accompany the data in the "Event" column. Each event represents a point in time where something notable has happened, for example when a stimulus was presented, or a keyboard response was received. Event markers may also contain metadata such as the system status or any errors that happened during the recording. Key event markers for each experiment are as follows:

AEP:
 - *trial-begin*
 - *oddball* or *target*
 - *trial-end*

AEP_Feedback:
- *trial-begin*
- *oddball* or *target*
- *response-received-arrow_down* or r*esponse-received-arrow_up*
- *response-was-correct* or *response-was-incorrect*
- _rt-*ms_ (reaction time in milliseconds, e.g., rt-200ms)
- *trial-end*

Resting_Open:
- *resting-state-eyes-open-begin*
- *resting-state-eyes-open-end*

Resting_Closed:
- *resting-state-eyes-closed-begin*
- *resting-state-eyes-closed-end*

## Raw Data 
  
Raw data contains unsegmented, unfiltered, and unprocessed data in CSV format. Each folder in "Raw_Data" that corresponds to one of the four experiment types will contain recordings from each subject.  
  
Recording files inside these folders are named as such: `{Subject ID}_{Experiment Type}_{Session ID}.csv`. For example, a resting state recording (with eyes open) from the first subject during the second session will have the name: `1_resting-open_2.csv`.  
  
Subjects are numbered from 1 through 10 and possible experiment types are aep/aep-feedback/resting-open/resting-closed. Session IDs are either 1 or 2 for "aep/aep-feedback" experiments, while all resting state experiments have a single session.  
  
Some recordings will have an additional '\_UNFINISHED' suffix at the end, which means that the recording was interrupted during that session (for example, due to the EEG device battery getting too low). All '\_UNFINISHED' recordings were re-run from start to finish, which means there are at least two full sessions for 'aep/aep-feedback' experiments. However, epochs from unfinished recordings do not have any defects and can be freely used in the subsequent steps of processing.

## Filtered Data  
  
The filtered data has the same CSV file format as the raw data. Only EEG channels are modified, other columns remain the same.  
  
Filtering of the EEG channels was done using the 0.5-60 Hz bandpass filter and 50 Hz notch filter. Both filters were designed with the MNE library as one-pass, zero-phase, non-causal filters using the windowed time-domain (firwin) method with a Hamming window.

## Epoched Data  
  
The raw data for each subject were segmented using the event markers, where all the data that was not involved in the trials (e.g. resting sections) were removed. For the "AEP" and "AEP_Feedback" experiments, segmented data epochs include the period from -0.2s before the stimulus. For the "Resting_Open" and "Resting_Closed" experiments, starting and ending points are cropped to the nearest event markers. The resulting epochs are stored in the "Epoched_Data" folder. No additional processing was done on the data except for the filtering process described above.  
  
Each epoch is stored in a separate CSV file while the multiple sessions are merged. Additionally, a suffix is added to the file name to indicate the stimulus type, which is either "standard" or "oddball". The naming convention for the files is as follows: `{Subject ID}_{Experiment Type}_{Epoch ID}_{Stimulus Type}.csv`.

## Selected Epochs  
  
The selected epochs are stored in the "Selected_Epochs" folder. The selected epochs are the epochs that were manually selected with the least noise. The selection process was done by visually inspecting the epochs and selecting the ones that were free of artifacts. The naming convention for the files is as follows: `{Subject ID}_{Experiment Type}_{Epoch ID}_{Stimulus Type}.csv`.  
  
The selected epochs in the "AEP" and "AEP_Feedback" experiments are baseline corrected using the 0.2s pre-stimulus period. The baseline correction is done by subtracting the mean of the pre-stimulus period from the entire epoch for each EEG channel. The epochs in the "Resting_Open" and "Resting_Closed" experiments are the same as in the "Epoched_Data" folder.

## Limitations

Data was recorded using the dry electrodes of the Unicorn Hybrid Black device. Although dry electrodes typically have a lower signal-to-noise ratio compared to wet electrodes, this choice was made for the sake of the practicality of the method. Additionally, the number of electrodes, subjects, and trials may pose limitations depending on the specific focus of the research.
