# spatialAudiopy: A Spatial Audio Framework

**spatialAudiopy** is a Python framework designed to simulate realistic spatial audio through the use of head-related transfer functions (HRTF). In this framework, the **Speaker** class is the core object that represents a sound source in a virtual space. It uses pre-measured HRTF data from the MIT Kemar dataset to accurately spatialize audio.

## The Speaker Class

The **Speaker** class encapsulates a sound source's properties and its spatialization process. When you create an instance of this class, you specify:

- **Azimuth (azi):** The horizontal angle in degrees at which the sound source is located relative to the listener.
- **Elevation (elev):** The vertical angle in degrees for the sound source.
- **Distance (dist):** The distance from the listener (this parameter can be used to further simulate distance effects).
- **Track:** The audio file to be spatialized.

### How It Works

1. **HRTF Data from MIT Kemar:**  
   The framework leverages the MIT Kemar HRTF dataset. This dataset contains impulse responses measured on a mannequin (Kemar) at different azimuths and elevations. The dataset is organized in folders (for example, `elev-40`, `elev0`, `elev10`, etc.) and the files are named according to the measured angles. The Speaker class uses these measurements to apply the appropriate HRTF to a given audio signal.

2. **Automatic HRIR Selection:**  
   Based on the desired azimuth and elevation, the Speaker class automatically selects the HRIR file that best matches these parameters. If a full 360° coverage is required but your available HRIRs only cover a limited azimuth range (e.g., 0° to 80°), the framework maps the given angle into the available range and—if necessary—flips the channels. This method ensures realistic spatial cues regardless of where the sound source is placed.

3. **Resampling and Convolution:**  
   To ensure that both the input audio and the HRIR share the same sample rate, the framework includes helper functions to resample the signals. Once the rates are aligned, the audio signal is convolved with the selected HRIR. This convolution creates a binaural effect, simulating the time delays and spectral modifications introduced by the listener’s head and ears.

## Example Usage

Here’s a short example of how you might use the Speaker class within your code:

```python
from spatialAudiopy import Speaker

# Create a speaker at a desired azimuth (in degrees), elevation, and provide the audio file.
sp1 = Speaker(azi=90, elev=0, dist=0, track="flute.mp3")

# Spatialize the audio file using the closest matching HRIR from the Kemar dataset.
sp1.spatialize()
