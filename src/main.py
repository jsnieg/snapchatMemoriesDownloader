import threading

from . import base

if __name__ == "__main__":
    config = base.Config()
    base.general_information(config=config)
    server_thread = threading.Thread(target=base.run_server, args=(config, ))
    beautifulSoup_thread = threading.Thread(target=base.run_beautiful_soup, args=(config, ))

    server_thread.start()
    beautifulSoup_thread.start()

    beautifulSoup_thread.join()