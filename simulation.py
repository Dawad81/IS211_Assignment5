#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" IS211_Assignment5"""


import argparse
import csv
import datetime
import urllib2


url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'


class Queue(object):
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Server(object):
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.process_time()


class Request(object):
    def __init__(self, time, request_time):
        self.timestamp = time
        self.request_time = request_time

    def get_stamp(self):
        return self.timestamp

    def process_time(self):
        return self.request_time

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulateOneServer(second_requested, time_needed):
    second_requested = int(second_requested)
    time_needed = int(time_needed)
    server = Server()
    queue = Queue()
    waiting_times = []
    request = Request(second_requested, time_needed)
    queue.enqueue(request)
    for current_second in range(second_requested):
        if (not server.busy()) and (not queue.is_empty()):
            next_task = queue.dequeue()
            waiting_times.append(next_task.wait_time(current_second))
            server.start_next(next_task)

        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %(average_wait, queue.size()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Enter a URL to begin.", required=True)
    #parser.add_argument("--servers", type=int, default=1)
    args = parser.parse_args()
    try:
        downloadcsvfile = urllib2.urlopen(args.file)
        reader = csv.reader(downloadcsvfile)
        lines = 0
        for row in reader:
            simulateOneServer(row[0], row[2])
    except:
        print 'An error has occured session terminated.\n\
        Exiting the program......Good Bye.'
        raise #SystemExit
    #else:
        #pass #processData(csvData)


if __name__ =='__main__':
    main()
