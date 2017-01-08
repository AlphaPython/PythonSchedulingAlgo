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


def get_Shortest_Job(queue,runCount):
    listProcesses = []
    add = True
    proess = queue.get()
    proe = proess
    for a in range(queue.qsize()):
        proess = queue.get()
        if add:
            listProcesses.append(proe)
            add = False

        print "Comparing Process Arrival Time: {} , and Cpu count: {}".format(proess.arrival_time , runCount)
        if proess.arrival_time <= runCount:
            print "Next Proc bust: {} , and Proc Bust: {}".format(proess.bust_time, proe.bust_time)
            if proess.bust_time <= proe.bust_time  and proess.arrival_time < proe.arrival_time:
                print "proe at before. {} ".format(proe.process_name)
                proe = proess
                print "proe at after. {} ".format(proe.process_name)

        listProcesses.append(proess)

    for pr in listProcesses:
        if proe != pr:
            print "going to queue : ",pr.process_name
            queue.put(pr)
    return proe


_readyQueue = Queue.Queue()
time_slice = 0

print 'Enter the number of processes: ',
no_of_process = integer_input()
print 'Enter the time Slice: ',
time_slice = integer_input()


fill_queue(_readyQueue )

cpuRunningCount = 0

print "*****************************************************************************************************"
print "* Process     Bust Time     Arrival Time     Start TIime     End Time     Turn Around      Waiting Time*"
while not _readyQueue.empty():


    prosess = get_Shortest_Job(_readyQueue,cpuRunningCount)
    print "Process Name : ",prosess.process_name
    print "Cpu Count {} and Process Arrival{}".format(cpuRunningCount,prosess.arrival_time)
    if(prosess.arrival_time > cpuRunningCount):
        cpuRunningCount += 1
        _readyQueue.put(prosess)
        continue

    if(not prosess.start_set):
        prosess.start_time = cpuRunningCount
        prosess.start_set = True

    if (prosess.bust_time == 0):
        prosess.end_time = cpuRunningCount
        print prosess.end_time
        print "*                                                                                     "
        print "*  {}                 {}          {}            {}                 {}                 {}         {}". \
            format(prosess.process_name, prosess.bust_time, prosess.arrival_time, prosess.start_time,
                   prosess.end_time, prosess.end_time - prosess.start_time,prosess.end_time- prosess._bust - prosess.start_time)
        continue
    print "running simply"
    cpuRunningCount += 1
    prosess.bust_time -= 1
    _readyQueue.put(prosess)

    print "****************************************************************************************************"