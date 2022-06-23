## Multithreading: Using mutex and semaphore to fix Race Conditions

In a simple search, the text is checked line by line and returns the line number in which the word was found.

In multi-threaded search, the text file is divided by the number of threads and each part is checked by one thread at a time. Because the threads run in parallel, they may find several threads of a word at the same time and want to print it in the output file, which causes a problem called a race condition. To solve this problem, we used mutex and semaphore to lock the source, which allows only one thread to take over the source at a time and perform the printing operation, and when done, release the source and the next thread. Lock it.
