import threading

from . import base

if __name__ == "__main__":
    # url_thread = threading.Thread(target=base.getWebPageText)
    server_thread = threading.Thread(target=base.runServer)
    beautifulSoup_thread = threading.Thread(target=base.runBeautifulSoup)

    server_thread.start()
    beautifulSoup_thread.start()

    beautifulSoup_thread.join()