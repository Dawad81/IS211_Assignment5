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
        self.items.insert(0, item)

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
    def __init__(self, second_requested, time_needed):
        self.timestamp = second_requested
        self.request_time = time_needed

    def get_stamp(self):
        return self.timestamp

    def process_time(self):
        return self.request_time

    def wait_time(self, second_requested):
        return self.timestamp - self.request_time


def simulateOneServer(downloadcsvfile):
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
    print"Average Wait %6.2f secs %3d tasks remaining." %(average_wait, queue.size())
    

def simulateManyServer(downloadcsvfile,num_server):
    serverdict={}
    server_list = []
    for num in range(0, int(num_server)):
        server_list.append(num)
    for server in server_list:
        #serverdict[server]= simulateOneServer(urllib2.urlopen(url))
        serverdict[server]= None
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
    print"Average Wait %6.2f secs %3d tasks remaining." %(average_wait, queue.size())


    #for server in server_list[::int(num_server)]:
        #serverdict[server]= queue.enqueue(request)
#[::int(nums_server)]
    print serverdict
#for i in range(team):
#    teamlist=players[i::team]
#    game.append(teamlist)
#    return game

test1 = simulateManyServer(urllib2.urlopen(url), 3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Enter a URL to begin.", required=True)
    #parser.add_argument("--servers", help="Enter the number of servers." required=False type=int, )
    args = parser.parse_args()
    try:
        #if args.file and args.server:
            #downloadcsvfile = urllib2.urlopen(args.file)
            #simulateManyServer(downloadcsvfile)
        #else:
        downloadcsvfile = urllib2.urlopen(args.file)
        simulateOneServer(downloadcsvfile)
    except:
        print 'An error has occured session terminated.\n\
        Exiting the program......Good Bye.'
        raise #SystemExit


if __name__ == '__main__':
    main()
