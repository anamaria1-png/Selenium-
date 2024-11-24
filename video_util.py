import ffmpeg  # Library for multimedia handling (audio/video)
import exception_handlers as eh  # Custom module for handling exceptions

import os  # Provides functions for interacting with the operating system


def video_audio_mux(path_audiosource, path_videosource, out_video_path):
    """
    Function to merge audio and video into a single file.

    Parameters:
    - path_audiosource: str - Path to the audio source file.
    - path_videosource: str - Path to the video source file.
    - out_video_path: str - Path to save the merged output video file.
    """
    try:
        # Alternative implementation using ffmpeg-python (commented out for clarity)
        # video = ffmpeg.input(path_videosource).video
        # audio = ffmpeg.input(path_audiosource).audio
        # ffmpeg.output(audio, video, out_video_path, vcodec='copy', acodec='copy').run()

        # Use the os.system call to execute an FFmpeg command
        os.system(f"ffmpeg -i {path_videosource} -i {path_audiosource} -c:v copy -c:a aac {out_video_path}")
    except ffmpeg.Error as e:
        # Handle ffmpeg-specific errors (e.g., file not found, format errors)
        eh.log("Unable to open video file")
    except PermissionError:
        # Handle cases where access to files is restricted
        eh.log("Unable to open video file")
        # eh.log will hande PermissionError


if __name__ == '__main__':
    # Example usage of the `video_audio_mux` function
    video_audio_mux("out.wav", "video.mp4", "out.mp4")


