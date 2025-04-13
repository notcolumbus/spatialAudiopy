import numpy as np
import matplotlib.pyplot as plt
import sys, glob
import soundfile as sf
import librosa
from scipy import signal


# Importing the MIT Kemar HRTF
HRTF_0 = glob.glob("hrtf/elev90/*.wav")
HRTF_10 = glob.glob("hrtf/elev80/*.wav")
HRTF_20 = glob.glob("hrtf/elev70/*.wav")
HRTF_30 = glob.glob("hrtf/elev60/*.wav")
HRTF_40 = glob.glob("hrtf/elev50/*.wav")
HRTF_50 = glob.glob("hrtf/elev40/*.wav")
HRTF_60 = glob.glob("hrtf/elev30/*.wav")
HRTF_70 = glob.glob("hrtf/elev20/*.wav")
HRTF_80 = glob.glob("hrtf/elev10/*.wav")
HRTF_90 = glob.glob("hrtf/elev0/*.wav")
HRTF_n10 = glob.glob("hrtf/elev-10/*.wav")
HRTF_n20 = glob.glob("hrtf/elev-20/*.wav")
HRTF_n30 = glob.glob("hrtf/elev-30/*.wav")
HRTF_n40 = glob.glob("hrtf/elev-40/*.wav")

def resample_signals(s1, f1, s2, f2):
    
    common_fs = max(f1, f2)
    if f1 != common_fs:
        s1 = resample_signal(s1, orig_sr=f1, target_sr=common_fs)
    if f2 != common_fs:
        s2 = resample_signal(s2, orig_sr=f2, target_sr=common_fs)
    print("Both signals resampled to:", common_fs, "Hz")
    return s1, common_fs, s2, common_fs

def resample_signal(signal_data, orig_sr, target_sr):

    if orig_sr == target_sr:
        return signal_data
    if signal_data.ndim == 1:
        return librosa.resample(signal_data, orig_sr=orig_sr, target_sr=target_sr)
    else:
        return librosa.resample(signal_data.T, orig_sr=orig_sr, target_sr=target_sr).T


class Speaker():
    
    def __init__(self, azi, elev, dist, track):
        self.azi = azi
        self.elev = elev
        self.dist = dist
        self.track = track

    def spatialise():
        print("hi")


if __name__ == "__main__":
    HRIR = HRTF_70[5]
    HRIR_data, fs = sf.read(HRIR)
    Audio, fs2 = sf.read("flute.mp3")
    print(HRIR_data.shape, fs)
    print(Audio.shape, fs2)
    resample_signals(HRIR_data, fs, Audio, fs2 )