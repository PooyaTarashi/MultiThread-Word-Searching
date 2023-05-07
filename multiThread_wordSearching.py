import threading
import os
from os.path import join, isdir
import time
import sys

# this variable will contain list of paths containing our file.
# we use multiple threads to update this variable
matches = []
# we should acquire this mutex when updating matches list
mutex = threading.Lock()


# every time we call file_search function, we should make a thread
# no mather it is a recursive call or it is an ordinary call
# we need to append all threads inside the function to a list and join them in a separate loop
def file_search(root: str, word: str) -> None:
    """
    :param root: The path to search in
    :param filename: the filename to search for
    :return: None
    """
    child_threads = []
    for file in os.listdir(root):
        full_path = join(root, file)  # concatenates root with file
        if isdir(full_path):
            t = threading.Thread(target=file_search, args=(full_path, word))
            t.start()
            child_threads.append(t)
        else:
            if file[-3:] == 'txt':
                with open(full_path, 'r') as f:
                    if word in f.read():
                        mutex.acquire()
                        matches.append(full_path)
                        mutex.release()
    for thread in child_threads:
        thread.join()


def main():
    b = time.time()
    path = 'C:\\Users\\Dell\\Desktop\\uni4012'
    t = threading.Thread(target=file_search, args=(path, 'IWantYou'))
    t.start()
    t.join()
    for m in matches:
        print('Matched:', m)
    print(f"Done, time taken: {round(time.time() - b, 2)} second(s)")


if __name__ == '__main__':
    main()