from datetime import datetime

log_filename = str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + "-log.txt"

def log(message: str):
    try:
        with open(log_filename, "a") as file:
            file.write(message + "\n")
    except PermissionError:
        print("Permission denied")

# there are 3 mode r for reading
# w - writing but it removes previous content
# and a for apending it allow you to write without removing the content
# this function is called multiple times if you were to use w you would only have the last written line