# Snapchat Memories Retriever
Python script to download your Snapchat memories when *you* download *your* data and choose what directory you wish to move them into.

## Prerequisites
Before downloading your data you must request your memories through Snapchat. Below you'll find steps through Computer Browser you must complete to obtain your memories.

After obtaining your data you only have 7 days to let this script run downloading and moving your files to your chosen directory if you fail to do so you must request new set of data from Snapchat.

1. Navigate to [Snapchat My Data](https://accounts.snapchat.com/v2/download-my-data) and Log In using your normal credentials.
![?](/assets/imageMemories.png)

2. Select `Export Your Memories` > `Request only Memories` and `All Time` in the data range to select all memories taken since your account's creation.
![?](/assets/imageIncludeAllTime.png)

3. Confirm your e-mail address and select `Submit` and you should get a notification on your Android/iOS device saying `Your Snapchat data is on its way!`.
![?](/assets/imageFinished.png)

4. Followed by **e-mail** from Snapchat with a instructions to download your memories in `mydata_<numbers>.zip` file.

## Usage
If using command-line:
- `python3 -m src.main --t "test_directory"`

## Running from Source

### Linux / WSL

To create a virtual environment:
- `python3 -m venv env/`

Activate it:
- `source /env/bin/activate`

Install all required packages to run the script in virutal environment:
- `(env) pip install -r ./requirements.txt`

To run the script from source:
- `(env) python3 -m src.main`