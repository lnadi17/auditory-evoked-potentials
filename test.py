from Recordings import Recordings
import matplotlib.pyplot as plt

plt.ion()  # Enable interactive mode

if __name__ == '__main__':
    basepath = './Recordings'
    recordings = Recordings(basepath)
