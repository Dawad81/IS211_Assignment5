#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" IS211_Assignment5"""


import argparse
import csv
import urllib2


URL = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'


class Queue(object):
    """This Queue class creates methods to enter data into a queue."""
    def __init__(self):
        """Constructor for Queue class."""
        self.items = []

    def is_empty(self):
        """Test if an item is equal to an empty list."""
        return self.items == []

    def enqueue(self, item):
        """Puts an item into a queue."""
        self.items.insert(0, item)

    def dequeue(self):
        """Removes an item from a queue."""
        return self.items.pop()

    def size(self):
        """Returns the amont of items in the Queue."""
        return len(self.items)


class Server(object):
    """This Server class simulates a server processing data from a queue."""
    def __init__(self):
        """Constructor for Server class."""
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        """Keeps track of time server takes."""
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        """Checks if the Server is busy."""
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        """Starts prcessing next task if server request is done."""
        self.current_task = new_task
        self.time_remaining = new_task.process_time()


class Request(object):
    """This Request class processes the time data was requested and the amount
    of time it takes to process the request."""
    def __init__(self, second_requested, time_needed):
        """Constructor for Request class."""
        self.timestamp = second_requested
        self.request_time = time_needed

    def get_stamp(self):
        """Records the second in which the request was given."""
        return self.timestamp

    def process_time(self):
        """Returns the time required to process the request."""
        return self.request_time

    def wait_time(self, second_requested):
        """Caluculates the wait time for the request."""
        return self.timestamp - self.request_time


def simulateOneServer(downloadcsvfile):
    """This function simulates one server, processing a csv fie of data request.

    Args:
        downloadcsvfile (file object): args to pars server request and the
        avrage time it takes to compleat processing all request.

    Returns:
        str: a string that caluclates the average wait time for all request in
        a csv file and how many task remain after the last reqest is received.

    Example:

        $ python simulation.py --file
        "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"

        >>> Average Wait 2501.00 secs 5006 tasks remaining.
    """
    reader = csv.reader(downloadcsvfile)
    server = Server()
    queue = Queue()
    waiting_times = []
    for current_second in reader:
        second_requested = int(current_second[0])
        time_needed = int(current_second[2])

        request = Request(second_requested, time_needed)
        queue.enqueue(request)
        if (not server.busy()) and (not queue.is_empty()):
            next_task = queue.dequeue()
            waiting_times.append(next_task.wait_time(second_requested))
            server.start_next(next_task)
        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print"Average Wait %6.2f secs %3d tasks remaining." %(average_wait,
                                                          queue.size())


def simulateManyServer(downloadcsvfile, num_server):
    """This function simulates many servers, processing a csv fie of data
    request divided amongst the number of servers entered.

    Args:
        downloadcsvfile (file object): args to pars server request and the
        avrage time it takes to compleat processing all request.
        num_server (int): the number of servers in simulation that will divided
        up the task of parsing the data in downloadcsvfile.

    Returns:
        str: a string that caluclates the average wait time for all request in
        a csv file to be processed by the servers entered,and how many task
        remain after the last reqest is received.

    Example:

        $ python simulation.py --file
        "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"
        --servers 3

        >>> Average Wait 5004.00 secs   0 tasks remaining.
    """
    server_list = []
    for num in range(0, int(num_server)):
        server_list.append([])
    reader = csv.reader(downloadcsvfile)
    server = Server()
    queue = Queue()
    waiting_times = []
    for current_second in reader:
        second_requested = int(current_second[0])
        time_needed = int(current_second[2])
        request = Request(second_requested, time_needed)
        queue.enqueue(request)
        for item in server_list:
            if (not server.busy()) and (not queue.is_empty()):
                next_task = queue.dequeue()
                waiting_times.append(next_task.wait_time(second_requested))
                server.start_next(next_task)
            server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print "Average Wait %6.2f secs %3d tasks remaining." %(average_wait,
                                                           queue.size())


def main():
    """ This function combines the simulateOneServer()  and simulateManyServer()
        into a single function to be run on the command line.

        main() dowloads a file from a provided --file, processes the data,
        then returns the results of simulateOneServer() if --servers is not
        specified.

        If --file and --servers is specified it returns the result of
        simulateManyServer() insted of simulateOneServer().

        If an impropper --url is input, an error message is raised and the
        program exits.

    Exsample:

        $ python simulation.py --file "http://"
        >>>An error has occured session terminated.
                    Exiting the program......Good Bye.



        simulateOneServer():

            $ python simulation.py --file
            "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"

            >>> Average Wait 2501.00 secs 5006 tasks remaining.

        simulateManyServer():

            $ python simulation.py --file
            "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"
            --servers 3

            >>> Average Wait 5004.00 secs   0 tasks remaining.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Enter a URL to begin.(required)",
                        required=True)
    parser.add_argument("--servers",
                        help="Enter the number of servers.(optional)",
                        required=False, type=int)
    args = parser.parse_args()
    try:
        if args.servers:
            downloadcsvfile = urllib2.urlopen(args.file)
            simulateManyServer(downloadcsvfile, args.servers)
        elif args.file:
            downloadcsvfile = urllib2.urlopen(args.file)
            simulateOneServer(downloadcsvfile)
    except:
        print 'An error has occured session terminated.\n\
        Exiting the program......Good Bye.'
        raise SystemExit


if __name__ == '__main__':
    main()
