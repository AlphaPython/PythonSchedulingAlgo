import process
import time
import Queue
import sys


def integer_input():
    number = 0
    while True:
        try:
            number = int(raw_input())
            break
        except ValueError:
            print 'Invalid Input. Plz Enter again: ',
    return number


def process_input(proces):
    process_instance = proces
    print 'Enter process {} Arrival Time: '.format(process_instance.process_name),
    process_instance.arrival_time = integer_input()
    print 'Enter process {} Bust Time: '.format(process_instance.process_name),
    process_instance.bust_time = integer_input()
    process_instance._bust = process_instance.bust_time
    return process_instance

def fill_queue(queue):
    arival_t = []
    count = 0
    arival_t.append(0)
    for eachprocess in range(no_of_process):
        count += 1
        process_instance = process.Process()
        process_instance.process_name = 'P' + str(eachprocess)
        process_input(process_instance)
        arival_t.append(process_instance.arrival_time)
        while arival_t[count - 1] > arival_t[count]:
            print 'Again! {} Arrival must be greator then previous: '\
                .format(process_instance.process_name),
            process_instance.arrival_time = integer_input()
            arival_t[count] = process_instance.arrival_time
        queue.put(process_instance)


def add_process_at_Valid_Postion_in_queue(queue,prosess,cpu_count):
    proc_list = []
    proc_added = False
    for number in range(queue.qsize()):
        check_process = queue.get()
        if(check_process.arrival_time > cpu_count and
           not proc_added):
            proc_list.append(prosess)
            proc_added = True
        proc_list.append(check_process)
    if(not proc_added):
        proc_list.append(prosess)
    for proc in proc_list:
        queue.put(proc)


_readyQueue = Queue.Queue()
time_slice = 0

print 'Enter the number of processes: ',
no_of_process = integer_input()
print 'Enter the time Slice: ',
time_slice = integer_input()


fill_queue(_readyQueue )



process_finished = False
cpuRunningCount = 0

print "*******************************************************************************************************"
print "* Process     Bust Time     Arrival Time     Start TIime     End Time     Turn Around       WaitingTime*"

while not _readyQueue.empty():

    prosess = _readyQueue.get()
    if(prosess.arrival_time > cpuRunningCount):
        cpuRunningCount = prosess.arrival_time

    if (not prosess.start_set):
        prosess.start_time = cpuRunningCount
        prosess.start_set = True

    for num in range(time_slice):
        process_finished = False

        if (prosess.bust_time == 0):
            process_finished = True
            prosess.end_time = cpuRunningCount
            break
        cpuRunningCount += 1
        prosess.bust_time -= 1

    if (not _readyQueue.empty() and prosess.bust_time != 0):
        add_process_at_Valid_Postion_in_queue(_readyQueue,prosess,cpuRunningCount)
        continue
    else:
        if _readyQueue.empty() and prosess.bust_time !=0:
            _readyQueue.put(prosess)

    if (prosess.bust_time == 0):
        if (prosess.end_time == 0):
            prosess.end_time = cpuRunningCount
            process_finished = True
        print "*                                                                                     *"
        print "*  {}                 {}          {}            {}                 {}                 {}         {} ". \
            format(prosess.process_name, prosess._bust, prosess.arrival_time, prosess.start_time,
                   prosess.end_time, prosess.end_time - prosess.start_time,prosess.end_time- prosess._bust - prosess.start_time)


print "*******************************************************************************************************"