from time import sleep
import os
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
import selenium.common.exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading as th

from audio_recorder import record_audio
from video_recorder import record_video
from audio_util import extract_audio_from_video, save_db_values
from video_util import video_audio_mux
from exception_handlers import log

# Path to the Chrome WebDriver executable
DRIVER_PATH = "./chromedriver.exe"

# Initialize the Selenium WebDriver service
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service)  # Create a new instance of Chrome WebDriver
driver.implicitly_wait(10)  # Set an implicit wait time of 10 seconds for element detection


def reject_cookies():
    """
    Function to reject cookie pop-ups on YouTube.
    """
    try:
        # Find cookie rejection buttons using their CSS selectors and click the first one
        elements = driver.find_elements(By.CSS_SELECTOR, "#dialog button.yt-spec-button-shape-next--mono")
        elements[0].click()
    except NoSuchElementException:
        # Handle cases where no cookie pop-up is found
        print("No cookie pop up found")
    except IndexError:
        log("No internet connection")
        driver.quit()


def play_youtube_video():
    """
    Function to play a YouTube video by automating browser interaction.
    """
    try:
        # Maximize the browser window and navigate to YouTube
        driver.maximize_window()

        log("Maximizing the window")
        driver.get("https://www.youtube.com/")
        log("Opening YouTube")
    except selenium.common.exceptions.WebDriverException:
        # Handle the case where there's no internet connection
        log("No internet connection")
        exit(1)  # Exit the program in case of an error
        # I haven't found a proper way to close a multithreaded application, this exit() will
        # only close the thread it's called on, one way to close the entire app is to call
        # os._exit() but this is not recommended

    # Wait for specific elements to load using WebDriverWait
    wait = WebDriverWait(driver, 30)
    reject_cookies()  # Call the function to reject cookie pop-ups
    log("Rejecting cookies")

    # Wait for the search bar to be clickable and perform a search
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#search')))
        search_bar = driver.find_element(By.CSS_SELECTOR, 'input#search')
        search_bar.click()  # Click on the search bar
        search_bar.send_keys("Skillet Victorious")  # Enter the search query
        log("Searching a song on YouTube")

    # Handle potential focus issues by clicking the search button twice
        sleep(3)
        driver.find_element(By.ID, "search-icon-legacy").click()
        driver.find_element(By.ID, "search-icon-legacy").click()

    # Wait for video titles to load and click the first video
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#video-title')))
        driver.find_elements(By.CSS_SELECTOR, 'a#video-title')[0].click()
        log("Clicking on the song")

    # Keep the browser open for 40 seconds to allow the video to play
        sleep(40)
        driver.quit()  # Close the browser after the video finishes playing
        log("Closing the web browser")
    # try it now
    except (IndexError, selenium.common.exceptions.WebDriverException):
        log("No internet connection")

def check_permissions():

    try:

        with open("test.txt", "r+") as f:
            f.write("test")
            f.close()
            os.remove("test.txt")
    except PermissionError:
        print("You don't have read or write permissions")
        exit()


def check_internet():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


# if there is no internet connection application will log that and exit
if not check_internet():
    log("No internet connection")# this will write to the log file if there is no internet connection
    exit()



# Start a thread to record audio for 60 seconds
record_audio_thread = th.Thread(target=record_audio, args=[60])
record_audio_thread.start()
log("Started audio recording")
# Start a thread to play the YouTube video
play_youtube_video_thread = th.Thread(target=play_youtube_video)
play_youtube_video_thread.start()

# Record video synchronously for 60 seconds
log("Started video recording")
record_video(60)

log("Ended video recording")
# Wait for the audio and video threads to finish
play_youtube_video_thread.join()
record_audio_thread.join()
log("Ended audio recording")

# Merge the recorded audio and video into a single output file
video_audio_mux(path_audiosource="audio.wav", path_videosource="video.mp4", out_video_path="out.mp4")
log("Combined audio and video into a single file")

# Optional: Remove the temporary video and audio files
# os.remove("audio.wav")
os.remove("video.mp4")
log("Removed video-only file")
os.remove("audio.wav")
log("Removed audio-only file")

# Extract audio data from the merged video file
audio_data = extract_audio_from_video("out.mp4")
log("Extracted audio data")
# Save the decibel (dB) values of the audio data to a text file
save_db_values("out.mp4", audio_data)
log("Saved db values to a file")

# I added another package to this project
# "requests" is the name of the package