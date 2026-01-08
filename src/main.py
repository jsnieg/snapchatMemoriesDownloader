import threading

# base.py and parser.py scripts
import base
import parser

if __name__ == "__main__":
    directory = parser.argument_parser()
    config = base.Config()
    config.target_dir = directory
    base.check_directories(config=config)
    base.dir_modified_date(config=config)
    server_thread = threading.Thread(target=base.run_server, args=(config, ))
    beautifulSoup_thread = threading.Thread(target=base.run_beautiful_soup, args=(config, ))

    server_thread.start()
    beautifulSoup_thread.start()

    beautifulSoup_thread.join()