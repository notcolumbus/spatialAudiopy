# spatialAudiopy: A Spatial Audio Framework

**spatialAudiopy** is a lightweight Python framework designed to simulate realistic spatial audio using head-related transfer functions (HRTF). It uses pre-measured HRIRs (Head-Related Impulse Responses) from the MIT Kemar dataset to spatialize audio, making it seem as if sounds are coming from specific directions in a virtual space.

## The Speaker Class

The **Speaker** class is the core building block of spatialAudiopy. It represents a sound source in 3D space by storing its direction and the audio file that will be spatialized.

### Constructor Parameters

When you create a Speaker object, you need to provide:

- **Azimuth (azi):**  
  This is a horizontal angle, in degrees, that tells you where the sound is coming from.  
  - **0°** means the sound is coming from directly in front of you.
  - **90°** means it is coming from your right.
  - **270° (or -90°)** means it is coming from your left.
  
  *Note:* The MIT Kemar HRTF dataset often has measurements for a limited range (typically from 0° to about 80°). If you specify an azimuth outside this range, the framework maps the angle into the available range and flips the HRIR channels if needed so that you can simulate 360° coverage.

- **Elevation (elev):**  
  This is the vertical angle, in degrees, of the sound source.  
  - **0°** means the sound is level with your ears.
  
  *Note:* The Kemar dataset provides HRIRs at specific elevation angles (e.g., -40, 0, 10, etc.). You can choose any value from 90(top) to -90(bottom), the Speaker class will automatically choose the most appropriate HRIR.

- **Distance (dist):**  
  This value indicates how far the sound source is from the listener. Although not fully implemented as of now.

- **Track:**  
  This is the audio file (for example, `"flute.mp3"`) that will be spatialized.

### How It Works

1. **HRTF Data from MIT Kemar:**  
   The Speaker class uses HRIR data from the MIT Kemar HRTF dataset. The dataset is organized in folders based on elevation (e.g., `elev-40`, `elev0`, `elev10`, etc.) and the files are named by their measured azimuth angles.

2. **Automatic HRIR Selection:**  
   When you specify an azimuth and elevation, the class automatically selects the HRIR file that best matches those angles. If your chosen azimuth falls outside the measured range (for example, a value above 180°), the code normalizes and flips it so that the correct HRIR is used.

3. **Resampling and Convolution:**  
   The audio track is resampled to match the HRIR’s sample rate. Then, the audio is convolved with the HRIR for both the left and right channels. This process mimics how sounds arrive at your ears with slight differences in time and frequency response.

## Example Usage

Below are a few simple examples of how to create Speaker objects and spatialize audio:

```python
from spatialAudiopy import Speaker

# Example 1: Sound coming from directly in front (0° azimuth, level with the ears)
speaker_front = Speaker(azi=0, elev=0, dist=0, track="flute.mp3")
speaker_front.spatialize()  # Simulates sound coming from the front.

# Example 2: Sound coming from the right (e.g., 60° azimuth)
speaker_right = Speaker(azi=60, elev=0, dist=0, track="flute.mp3")
speaker_right.spatialize()  # Simulates sound coming from your right side.

# Example 3: Sound from an extreme angle (e.g., 250° azimuth)
# Here, 250° is normalized and flipped to simulate sound from the left.
speaker_left = Speaker(azi=250, elev=0, dist=0, track="flute.mp3")
speaker_left.spatialize()  # Simulates sound coming from your left side.
