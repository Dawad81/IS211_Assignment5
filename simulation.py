#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" IS211_Assignment5"""


import argparse
import csv
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
    def __init__(self, ppm):
        self.page_rate = ppm
       
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
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate


class Request(object):
    def __init__(self, time):
        self.timestamp = time
        #self.pages = random.randrange(1, 21)

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulateOneServer(num_seconds, time) pages_per_minute):
    server = Server(time) #(pages_per_minute)
    request = Queue()
    waiting_times = []
    for current_second in range(num_seconds):
        if new_print_task():
            task = Task(current_second)
            print_queue.enqueue(task)

        if (not lab_printer.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time(current_second))
            lab_printer.start_next(next_task)

        lab_printer.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %(average_wait, print_queue.size()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Enter a URL to begin.", required=True)
    #parser.add_argument("--servers", help="Enter # of servers to be used.", type=int, required= false, default=1)
    args = parser.parse_args()
    try:
        downloadcsvfile = urllib2.urlopen(url)
        reader = csv.reader(downloadcsvfile)
        lines = 0
        for row in reader:
            simulateOneServer(args.file) #csvData = downloadData(args.url)
    except:
        print 'An error has occured session terminated.\n\
        Exiting the program......Good Bye.'
        raise SystemExit
    else:
        pass #processData(csvData)
