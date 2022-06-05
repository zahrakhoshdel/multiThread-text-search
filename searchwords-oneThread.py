import logging
import time
import sys


def search_function(file, string_to_search):

    # time.sleep(0.01)

    # string_to_search = 'salam'
    start = time.perf_counter()

    words = string_to_search.split(" ")
    #print("words1 : \n", words)

    Counter = 0
    CoList = file.split("\n")

    for i in CoList:
        Counter += 1
        for word in words:
            if (i.find(word) > -1):

                finish = time.perf_counter()

                finish_write = time.perf_counter()
                write_to_file(word, Counter, round(
                    finish-start, 2), round(finish_write-start, 2))

                print("*found word %s at line: %d\n" %
                      (word, Counter))
                break

        #Counter = 0
    # print("THREAD '%d' FOUND \n" % (index, ))
    return


def get_file_lines(filename):
    file = open(filename, "r")
    number_of_lines = 0

    for line in file:
        line = line.strip("\n")
        number_of_lines += 1
    return number_of_lines


def write_to_file(word, line, time, wtime):
    f = open('output.txt', 'a')
    f.write("this found word '%s' at line: %s in %s secound and write %s sec\n" %
            (word, line, time, wtime))
    f.close()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

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

    s = time.perf_counter()
    # Welcome screen
    print("\n            WELCOME\n")
    print("  ------------=========--------------\n")
    NLines = get_file_lines(filename)
    print("This is the number of lines in the file", NLines)

    search_function(text, words)

    e = time.perf_counter()
    print("time exe: ", round(e-s, 2))
    f.close()
