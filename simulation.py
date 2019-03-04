#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" IS211_Assignment5"""


import argparse
import csv
import urllib2


url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'


class Queue(object):
    """Docstring."""
    def __init__(self):
        """Constructor for Queue class."""
        self.items = []

    def is_empty(self):
        """Docstring."""
        return self.items == []

    def enqueue(self, item):
        """Docstring."""
        self.items.insert(0, item)

    def dequeue(self):
        """Docstring."""
        return self.items.pop()

    def size(self):
        """Docstring."""
        return len(self.items)

class Server(object):
    """Docstring"""
    def __init__(self):
        """Constructor for Server class."""
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        """Docstring."""
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        """Docstring."""
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        """Docstring."""
        self.current_task = new_task
        self.time_remaining = new_task.process_time()


class Request(object):
    """Docstring"""
    def __init__(self, second_requested, time_needed):
        """Constructor for Request class."""
        self.timestamp = second_requested
        self.request_time = time_needed

    def get_stamp(self):
        """Docstring."""
        return self.timestamp

    def process_time(self):
        """Docstring."""
        return self.request_time

    def wait_time(self, second_requested):
        """Docstring."""
        return self.timestamp - self.request_time


def simulateOneServer(downloadcsvfile):
    """Docstring"""
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
    """Docstring"""
    serverdict = {}
    server_list = []
    for num in range(0, int(num_server)):
        server_list.append([])
    #print server_list
    #for server in server_list:
        #serverdict[server]= simulateOneServer(urllib2.urlopen(url))
        #serverdict[server]= []
    reader = csv.reader(downloadcsvfile)
    server = Server()
    queue = Queue()
    waiting_times = []
    #for current_second in reader:
    #for item in server_list:
    for current_second in reader:
        #for item in server_list:
        second_requested = int(current_second[0])
        time_needed = int(current_second[2])
        request = Request(second_requested, time_needed)
        queue.enqueue(request)
        #roundrobin=request[::int(num_server)]
        #for item in server_list:
            #for i in range(num_server)
                #queue_request = queue.enqueue(request)
            #server_list[::num_server].append(queue_request)
                #item.append(queue_request)
        #print server_list
        for item in server_list:
            if (not server.busy()) and (not queue.is_empty()):
                next_task = queue.dequeue()
                waiting_times.append(next_task.wait_time(second_requested))
                server.start_next(next_task)
            server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print "Average Wait %6.2f secs %3d tasks remaining." %(average_wait,
                                                           queue.size())
        #item.append(wait)
    #print server_list
    #for server in server_list[::int(num_server)]:
        #serverdict[server]= queue.enqueue(request)
#[::int(num_server)]
    #print serverdict
#for i in range(num_server):
#    list=current_second[i::num_server]
#    item.append(list)
#    return game

#test1 = simulateManyServer(urllib2.urlopen(url), 2)


def main():
    """Docstring"""
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
