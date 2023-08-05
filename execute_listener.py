import subprocess
import time


def start_script(script_path):
    # Start the script as a subprocess
    process = subprocess.Popen(["python", script_path])
    return process


def stop_script(process):
    # Stop the script subprocess
    process.terminate()


if __name__ == "__main__":
    # Replace 'your_script.py' with the path to your actual script
    script_path = "/home/hp/Desktop/Projects/anypli-ftour/skype_listener.py"

    # Replace 60 with the duration in seconds that you want the script to run
    duration = 60

    print("Script started:", time.strftime("%Y-%m-%d %H:%M:%S"))

    # Start the script
    process = start_script(script_path)

    # Wait for the specified duration
    time.sleep(duration)

    # Stop the script after the specified duration
    stop_script(process)

    print("Script ended:", time.strftime("%Y-%m-%d %H:%M:%S"))
