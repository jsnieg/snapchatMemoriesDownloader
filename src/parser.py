import argparse

# window.py script
import window

def argument_parser() -> str:
    """Parser for the commands when running the script through CLI."""
    description = f'Snapchat Memories Retriever.\nDownload your memories onto your device and move them to directory of your choosing.'
    parser = argparse.ArgumentParser(description=description)

    # change required around eventually...
    parser.add_argument('--window', '--w', type=bool,
                        help='Window flag to open the Python script with GUI window to choose where to move your files into after download.', required=False)

    parser.add_argument('--target', '--t', type=str,
                        help='Target directory (as string) you wish to put your memories into.\nOpen up your file explorer and copy the filepath of directory you wish to transfer your memories into after download is completed.', required=False)
    #parser.print_help()

    args = parser.parse_args()

    if args.window:
        target_directory = window.show_window()
    else:
        target_directory = args.target

    print(target_directory)
    # return target_directory