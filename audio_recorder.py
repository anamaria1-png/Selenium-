import soundcard as sc  # Library for audio input/output
import soundfile as sf  # Library for reading and writing audio files
import exception_handlers as eh  # Custom module for handling exceptions


def record_audio(sec):
    """
    Records audio from the default speaker using loopback.

    Parameters:
    - sec (int): The duration (in seconds) for which audio will be recorded.
    """
    OUTPUT_FILE_NAME = "audio.wav"  # Name of the output audio file
    SAMPLE_RATE = 44100  # Sampling rate for the audio recording
    RECORD_SEC = sec  # Duration of the recording in seconds

    try:
        # Set up the microphone using the default speaker with loopback enabled
        with sc.get_microphone(
            id=str(sc.default_speaker().name),  # Retrieve the default speaker's name
            include_loopback=True  # Enable loopback to record speaker output
        ).recorder(samplerate=SAMPLE_RATE) as mic:
            # Record audio for the specified duration
            audio_data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)

            # Save the recorded audio to a file
            sf.write(file=OUTPUT_FILE_NAME, data=audio_data[:, 0], samplerate=SAMPLE_RATE)

            # Notify the user that the recording is complete
            print("Audio recording complete.")
    except (sf.SoundFileError, IOError) as e:
        # Handle any exceptions and display an error message
        eh.log(f"Error recording audio: {e}")
