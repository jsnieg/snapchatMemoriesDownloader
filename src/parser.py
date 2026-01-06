import argparse


def argument_parser() -> str:
    """Parser for the commands when running the script through CLI."""
    description = f'Snapchat Memories Retriever.\nDownload your memories onto your device and move them to directory of your choosing.'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--target', '--t', type=str,
                        help='Target directory (as string) you wish to put your memories into.\nOpen up your file explorer and copy the filepath of directory you wish to transfer your memories into after download is completed.')
    #parser.print_help()

    args = parser.parse_args()

    target_directory: str = args.target

    # if target_directory is not type(str):
    #     assert False, "Target directory was not specified."

    return target_directory