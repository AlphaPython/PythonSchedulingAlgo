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


def process_input(proces,take_io):
    process_instance = proces
    if take_io:
        print 'Enter IO Bust For Process {}: '.format(process_instance.process_name),
        process_instance.io_bust = integer_input()
        print 'Enter IO interrupt time forProcess {}: '.format(process_instance.process_name),
        process_instance.io_interrupt_time = integer_input()
    print 'Enter process {} Arrival Time: '.format(process_instance.process_name),
    process_instance.arrival_time = integer_input()
    print 'Enter process {} Bust Time: '.format(process_instance.process_name),
    process_instance.bust_time = integer_input()
    return process_instance


def fill_queue(queue,io_bbust,io_interrupt,choice):
    odd = False
    even = False
    all = False
    if choice == 1:
        odd = True
    if choice == 2:
        even = True
    if choice == 3:
        all = True
    arival_t = []
    count = 0
    arival_t.append(0)
    for eachprocess in range(no_of_process):
        count += 1
        process_instance = process.Process()
        if((eachprocess+1) % 2 == 0 and even):
            process_instance.io_bust = io_bbust
            process_instance.io_interrupt_time = io_interrupt
        if((eachprocess+1) % 2 == 1 and odd):
            process_instance.io_bust = io_bbust
            process_instance.io_interrupt_time = io_interrupt
        process_instance.process_name = 'P' + str(eachprocess + 1)
        process_input(process_instance,all)
        arival_t.append(process_instance.arrival_time)
        while arival_t[count - 1] > arival_t[count]:
            print 'Again! {} Arrival must be greator then previous: ' \
                .format(process_instance.process_name),
            process_instance.arrival_time = integer_input()
            arival_t[count] = process_instance.arrival_time
        queue.put(process_instance)

def peek(queue):
    queu = queue
    proc = queu.get()
    return proc

def add_process_at_Valid_Postion_in_queue(queue,prosess,cpu_count):
    proc_list = []
    proc_added = False
    for number in range(queue.qsize()):
        check_process = queue.get()
        if(check_process.arrival_time > cpu_count and
           not proc_added and check_process.arrival_time > prosess.arrival_time):
            proc_list.append(prosess)
            proc_added = True
        proc_list.append(check_process)
    if(not proc_added):
        proc_list.append(prosess)
    for proc in proc_list:
        queue.put(proc)


def take_choice(range):
    choic = 0
    check = False
    while(True):
        if check:
            print 'Not Valid Choice: ',
        check = True
        choic = integer_input()
        if choic <= range and choic > 0:
            break
    return choic

_readyQueue = Queue.Queue()
_waitingQueue = Queue.Queue()
_auxilaryQueue = Queue.Queue()
time_slice = 0

print 'Enter the number of processes: ',
no_of_process = integer_input()
print 'Enter the time Slice: ',
time_slice = integer_input()

print 'Select the type of input output bust: ' \
      '\n1 => Odd Processes' \
      '\n2 => Even Processes' \
      '\n3 => Different for All Processes' \
      '\n\nEnter your Choice:',

choice = take_choice(3)
print 'take choice'
io_bust = 0
_io_interrupt = 0
if choice == 1 or choice == 2:
    print "IO Bust for all process : ",
    io_bust = integer_input()
    print "io_interrupt for all process : ",
    _io_interrupt = integer_input()

fill_queue(_readyQueue,io_bust,_io_interrupt,choice )



process_finished = False
cpuRunningCount = 0

print "*************************************************************************************************"
print "* Process     Bust Time     Arrival Time     Start TIime     End Time     Turn Around   WaitingTime  *"


while not _readyQueue.empty():

    prosess = _readyQueue.get()
    prosess._added = False
    print "Process :{}".format(prosess.process_name)
    print "arrival : ",prosess.arrival_time
    print "time slice : ",prosess.done_time_slice
    if(prosess.arrival_time > cpuRunningCount):
        print "Waiting for process arrival at {}!".format(cpuRunningCount)
        time.sleep(prosess.arrival_time - cpuRunningCount)
        cpuRunningCount = prosess.arrival_time
        print "Running at : {}".format(cpuRunningCount)

    if (not prosess.start_set):
        prosess.start_time = cpuRunningCount
        prosess.start_set = True

    if prosess.done_time_slice == time_slice:
        prosess.done_time_slice = 0

    for num in range(time_slice):
        process_finished = False

        if not _waitingQueue.empty():
            top_process = peek(_waitingQueue)
            if top_process.arrival_time == cpuRunningCount:
                top_process = _waitingQueue.get()
                _auxilaryQueue.put(top_process)

        if (prosess.bust_time == 0):
            process_finished = True
            prosess.end_time = cpuRunningCount
            break

        if prosess.io_interrupt_time == prosess.io_int_count:
            prosess.io_int_count = 0
            print "Interrupting Process :{}".format(prosess.process_name)
            prosess.arrival_time = cpuRunningCount + prosess.io_bust
            print 'new arrival ',prosess.arrival_time
            print 'Adding to waiting Queue'
            prosess._added = True
            _waitingQueue.put(prosess)
            break
        if prosess.done_time_slice == time_slice:
            prosess.done_time_slice = 0
            print 'Slice ended at: ',cpuRunningCount
            break

        print "Process Running! : {}".format(prosess.process_name)
        cpuRunningCount += 1
        prosess.io_int_count += 1
        prosess.done_time_slice += 1
        prosess.bust_time -= 1
        prosess.arrival_time = cpuRunningCount
        #time.sleep(1)

    while not _auxilaryQueue.empty():
        aux_proc = _auxilaryQueue.get()
        aux_proc.arrival_time = 0
        add_process_at_Valid_Postion_in_queue(_readyQueue, aux_proc, cpuRunningCount)

    if (not _readyQueue.empty() and prosess.bust_time != 0 and (not prosess._added)):
        print 'Loop Skipped at , ',cpuRunningCount
        add_process_at_Valid_Postion_in_queue(_readyQueue,prosess,cpuRunningCount)
        print 'size of the ready queue : ',_readyQueue.qsize()
        continue
    else:
        if _readyQueue.empty() and prosess.bust_time !=0 and (not prosess._added):
            _readyQueue.put(prosess)
            continue
    if _readyQueue.empty():
        _readyQueue = _waitingQueue
        _waitingQueue.queue.clear()

    if (prosess.bust_time == 0):
        if (prosess.end_time == 0):
            prosess.end_time = cpuRunningCount
            process_finished = True
        print "*                                                                                     "
        print "*  {}                 {}          {}            {}                 {}                {}         {} ". \
            format(prosess.process_name, prosess._bust, prosess.arrival_time, prosess.start_time,
                   prosess.end_time, prosess.end_time - prosess.start_time,prosess.end_time- prosess._bust - prosess.start_time)
print "**************************************************************************************************"