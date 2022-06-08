import logging
import math
import threading
import time
import os
import sys


def thread_function(mutex, index, NTLine, string_to_search, file):
    #logging.info("Thread %s: starting", index)

    # time.sleep(0.01)
    sum = 0

    start = time.perf_counter()

    words = string_to_search.split(" ")

    # The starting line of each thread
    for n in range(0, index):
        sum = sum + NTLine[n]

    Counter = 0
    CoList = file.split("\n")
    #print("col: ", CoList)

    for i in CoList:
        Counter += 1
        for word in words:
            if (i.find(word) > -1):

                finish = time.perf_counter()
                #print("t %d found %s: " % (index, word))
                ns = sum + Counter

                mutex.acquire()
                finish_write = time.perf_counter()
                write_to_file(index, word, ns, round(
                    finish-start, 2), round(finish_write-start, 2))
                mutex.release()

                # print("*thread '%d' found word %s at line: %d\n" %
                #       (index, word, ns))
                break

        #Counter = 0
    # print("THREAD '%d' FOUND \n" % (index, ))
    return


def NLines_thread(file, index):
    lin = len(file.splitlines())-1
    #print("t %d has %d line \n" % (index, lin))
    return lin


def get_file_lines(filename):
    file = open(filename, "r")
    number_of_lines = 0

    for line in file:
        line = line.strip("\n")
        number_of_lines += 1
    file.close()
    return number_of_lines


def write_to_file(index, word, line, time, wtime):
    f = open('output_mutex.txt', 'a')
    f.write("thread '%d' found word %s at line: %s in %s secound and write to file in %s sec\n" %
            (index, word, line, time, wtime))
    f.close()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    THREAD_NUMBER = 4

    filename = input("Enter file name(like test.txt): ")
    print("Filename is: " + filename)

    try:
        with open(filename, 'r') as f:
            text = f.read()
    except OSError:
        print("Could not open/read file:", filename)
        sys.exit()

    words = input("Enter words(like one two three): ")
    print("words : " + words)

    # Welcome screen
    print("\n            WELCOME\n")
    print("  ------------=========--------------\n")
    print("\nThread number: ", THREAD_NUMBER)

    NLines = get_file_lines(filename)
    print("number of lines in this file", NLines)

    fSize = os.stat(filename).st_size
    chunk = math.ceil((fSize / THREAD_NUMBER))
    print("File size of the source file: ", fSize)
    # print('chunk: ', chunk)

    # Number of lines each thread
    NTLine = []
    for index in range(THREAD_NUMBER):
        ntle = NLines_thread(
            text[int(index * chunk):int((index+1) * chunk)-1], index)
        NTLine.append(ntle)
    #print("number of line each thread:", NTLine)

    s = time.perf_counter()

    mutex_lock = threading.Lock()
    threads = list()
    for index in range(THREAD_NUMBER):
        #logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(mutex_lock,
                                                           index, NTLine, words, text[int(index * chunk):int((index+1) * chunk)]))
        threads.append(x)
        x.daemon = True
        x.start()

    for index, thread in enumerate(threads):
        #logging.info("Main    : before joining thread %d.", index)
        thread.join()
        #logging.info("Main    : thread %d done", index)
    e = time.perf_counter()
    print("time exe: ", round(e-s, 2))
    f.close()
