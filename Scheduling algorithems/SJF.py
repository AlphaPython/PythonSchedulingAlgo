import process
import time
import Queue

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

def get_Shortest_Job(queue,runCount):
    listProcesses = []
    add = True
    proess = queue.get()
    proe = proess
    size = queue.qsize()
    for a in range(size):
        proess = queue.get()
        if add:
            listProcesses.append(proe)
            add = False
        if proess.arrival_time <= runCount:
            if proess.bust_time < proe.bust_time:
                proe = proess
        listProcesses.append(proess)


    for pr in listProcesses:
        if proe != pr:
            queue.put(pr)
    return proe



_readyQueue = Queue.Queue()
time_slice = 0

print 'Enter the number of processes: ',
no_of_process = integer_input()

fill_queue(_readyQueue )

cpuRunningCount = 0

print "*************************************************************************************** "
print "* Process     Bust Time     Arrival Time     Start TIime     End Time     Turn Around   *"
while not _readyQueue.empty():

    prosess = get_Shortest_Job(_readyQueue,cpuRunningCount)
    if(prosess.arrival_time > cpuRunningCount):
        cpuRunningCount  = prosess.arrival_time
        _readyQueue.put(prosess)
        continue

    prosess.start_time = cpuRunningCount
    cpuRunningCount += prosess.bust_time
    prosess.end_time = cpuRunningCount
    print "*                                                                                     *"
    print "*  {}                 {}          {}            {}                 {}                 {}   ".\
        format(prosess.process_name,prosess.bust_time,prosess.arrival_time,prosess.start_time,
               prosess.end_time,prosess.end_time-prosess.start_time)

print "****************************************************************************************"