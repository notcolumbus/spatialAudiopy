import numpy as np
import  glob
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
    """
    Finds the closest HRIR file based on desired azimuth and elevation.
    Also returns a flag indicating whether the HRIR should be flipped for proper 360° coverage.
    """
    desired_azi_norm = desired_azi % 360

    # If the normalized azimuth is greater than 180, flip is needed.
    if desired_azi_norm > 180:
        effective_azi = 360 - desired_azi_norm
        flip_flag = True
    else:
        effective_azi = desired_azi_norm
        flip_flag = False

    # Use effective_azi for selecting the HRIR file.
    root_path = "hrtf"
    folders = sorted(glob.glob(os.path.join(root_path, "elev*")))
    if not folders:
        raise FileNotFoundError(f"No elevation folders found in {root_path}")
    
    # Choose the folder with elevation closest to desired_elev.
    elev_diffs = {}
    for folder in folders:
        elev_val = parse_elev(os.path.basename(folder))
        elev_diffs[folder] = abs(elev_val - desired_elev)
    chosen_elev_folder = min(elev_diffs, key=elev_diffs.get)
    
    # List all .wav files in that folder.
    wav_files = sorted(glob.glob(os.path.join(chosen_elev_folder, "*.wav")))
    if not wav_files:
        raise FileNotFoundError(f"No .wav files found in folder {chosen_elev_folder}")
    
    # Use the effective azimuth as target for comparison.
    target_azi = effective_azi
    angle_diffs = {}
    for wav_file in wav_files:
        angle_val = parse_angle(wav_file)
        angle_diffs[wav_file] = abs(angle_val - target_azi)
    closest_file = min(angle_diffs, key=angle_diffs.get)
    
    return closest_file, flip_flag

class Speaker():
    def __init__(self, azi, elev, dist, track):
        self.azi = azi
        self.elev = elev
        self.dist = dist
        self.track = track

    def spatialize(self):
        HRIR, flip_flag = get_HRIR(self.azi, self.elev)
        print(f"Selected HRIR: {HRIR} (Flip: {flip_flag})")
        
        # Read the HRIR file.
        HRIR_data, fs = sf.read(HRIR)

        # Flip HRIR if needed.
        if flip_flag:
            HRIR_data = np.flip(HRIR_data, axis=1)

        Audio, fs2 = sf.read(self.track)
        # Converting user submitted track to mono for convolution
        if Audio.shape[1] >1:
            audio_mono = np.mean(Audio, axis = 1)
        else:
            audio_mono = Audio

        # Resample signals to ensure sample rates are identical.
        HRIR_data, common_fs, audio_mono, common_fs = resample_signals(HRIR_data, fs, audio_mono, fs2)

        # Convolving the impulse respons with the Audio track
        signal_L = np.convolve(audio_mono, HRIR_data[:,0])
        signal_R = np.convolve(audio_mono, HRIR_data[:,1])

        # Generating audio file from both channels
        spatial_mix = np.vstack([signal_L, signal_R]).transpose()
        sf.write("krish.wav", spatial_mix, common_fs)



if __name__ == "__main__":
    sp1 = Speaker(40, 40, 0, "679.mp3")
    sp1.spatialize()
