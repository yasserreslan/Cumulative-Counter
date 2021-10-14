# Car Cumulative counter

This cumulative counter is a tool built using Python to count cars crossing the yellow line in the given video. 

## Overview
The car cumulative counter was created with both python open source libraries Imutils and OpenCv. The AI searches for boxes in frame with settings set to identify cars shapes based on minimum and maximum box area and cars that are moving by comparing the current frame with previous frames. The appropriate video will be automatically provided to the virtual environment with the help of Pytube, which will download the video frames upon running.


## Usage
After cloning the repository enter the following commands into the command shell of your virtual environment.

```bash
pip install -r requirements.txt
python main.py
```

Upon running the previous commands into your command shell, Pytube will be responsible of downloading the appropriate video required for the car recognition test. Running time may differ based on internet speeds since download is required.

## References 
This code is written in accordance to the PEP8 Style Guide for Python Code

[PEP8](https://www.python.org/dev/peps/pep-0008/)
