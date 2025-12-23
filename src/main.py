import threading

from . import base

if __name__ == "__main__":
    # url_thread = threading.Thread(target=base.getWebPageText)
    server_thread = threading.Thread(target=base.run_server)
    beautifulSoup_thread = threading.Thread(target=base.run_beautiful_soup)

    server_thread.start()
    beautifulSoup_thread.start()

    beautifulSoup_thread.join()