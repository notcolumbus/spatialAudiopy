import numpy as np
import matplotlib.pyplot as plt
import sys, glob
import soundfile as sf
import librosa
from scipy import signal
import os

# Helper functions
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

def nround(x, base=10):
    return base * round(float(x) / base)


def parse_elev(folder_name):
    elev_str = folder_name.replace("elev", "")
    return int(elev_str)

def parse_angle(filename):
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    e_idx = name.find('e')
    a_idx = name.rfind('a')
    angle_str = name[e_idx+1:a_idx]
    return int(angle_str)

def get_HRIR(desired_azi, desired_elev):
    root_path = "hrtf"
    folders = sorted(glob.glob(os.path.join(root_path, "elev*")))
    if not folders:
        raise FileNotFoundError(f"No elevation folders found in {root_path}")
    elev_diffs = {}
    for folder in folders:
        elev_val = parse_elev(os.path.basename(folder))
        elev_diffs[folder] = abs(elev_val - desired_elev)
    chosen_elev_folder = min(elev_diffs, key=elev_diffs.get)
    wav_files = sorted(glob.glob(os.path.join(chosen_elev_folder, "*.wav")))
    if not wav_files:
        raise FileNotFoundError(f"No .wav files found in folder {chosen_elev_folder}")
    target_azi = abs(desired_azi)
    angle_diffs = {}
    for wav_file in wav_files:
        angle_val = parse_angle(wav_file)
        angle_diffs[wav_file] = abs(angle_val - target_azi)
    closest_file = min(angle_diffs, key=angle_diffs.get)
    return closest_file

class Speaker():
    def __init__(self, azi, elev, dist, track):
        self.azi = azi
        self.elev = elev
        self.dist = dist
        self.track = track

    def spatialise(self):
        HRIR = get_HRIR(self.azi,self.elev)
        print(HRIR)
        HRIR_data, fs = sf.read(HRIR)
        Audio, fs2 = sf.read(self.track)
        resample_signals(HRIR_data, fs, Audio, fs2 )


if __name__ == "__main__":
    sp1 = Speaker(999,0,0,"flute.mp3")
    sp1.spatialise()