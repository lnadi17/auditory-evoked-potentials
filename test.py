from Recordings import Recordings

if __name__ == '__main__':
    basepath = './Recordings'
    recordings = Recordings(basepath)
    recordings.print_info(group='*', session='*', subject_id='*', experiment_id='aep_feedback')
