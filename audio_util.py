import ffmpeg
import numpy as np
import exception_handlers as eh


def extract_audio_from_video(video_filepath):
    try:
        # Extract audio with ffmpeg
        out, err = ffmpeg.input(video_filepath) \
            .output('pipe:1', format='wav') \
            .run(capture_stdout=True, capture_stderr=True)

        # Convert audio data to numerical values
        audio_data = np.frombuffer(out, np.int16)
        return audio_data

    except ffmpeg.Error as e:
        eh.log("ffmpeg is unable to open the video")# more exceptions here needed too:((
        return None
    except PermissionError:
        return None
    except FileNotFoundError:
        eh.log(video_filepath + " does not exist")
    except OSError:
        eh.log("ffmpeg not found or failed to execute.")



def save_db_values(video_filepath, audio_data):
    audio_data = extract_audio_from_video(video_filepath)

    if audio_data is not None:
        print("Audio data successfully extracted")
        epsilon = 1e-10
        audio_data_db = 20 * np.log10(np.abs(audio_data) + epsilon)

        try:
            with(open("db_values.txt", "w")) as f:
                for i in audio_data_db:
                    f.write(str(i) + "\n")
        except PermissionError:
            eh.log("Unable to write to db values to a text file")


if __name__ == "__main__":
    extract_audio_from_video("video.mp4")