import sys
import threading
import time
from datetime import datetime

def handle(id):
    # 模拟CPU计算密集型程序
    start = datetime.now()
    while True:
        end = datetime.now()
        if (end- start).seconds > 1:
            break
    # 模拟IO密集型程序
    time.sleep(1)

def multi_thread(ids, thread_num):
    # 按照长度进行分组
    for i in range(0, len(ids), thread_num):
        group_ids = ids[i:i + thread_num]
        threads = []
        for id in group_ids:
            thread = threading.Thread(target=handle, args=(id,))
            threads.append(thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

def multi_process(ids, proc_num, thread_num):
    from multiprocessing import cpu_count, Pool
    proc_pool = Pool(processes=proc_num)
    group_count = int(len(ids)/proc_num)
    for i in range(0, len(ids), group_count):
        proc_pool.apply_async(
            func=multi_thread,
            args=(
                ids[i:i + group_count],
                thread_num,
            )
        )

    proc_pool.close()
    proc_pool.join()

if __name__ == "__main__":
    ids = [i for i in range (0, 100)]
    proc_num = int(sys.argv[1])
    thread_num = int(sys.argv[2])

    start = datetime.now()
    multi_process(ids, 100, 1)
    end = datetime.now()
    print("多进程耗时:{} s".format((end - start).seconds))

    start = datetime.now()
    multi_process(ids, 1, 100)
    end = datetime.now()
    print("多线程耗时:{} s".format((end - start).seconds))

    start = datetime.now()
    multi_process(ids, 10, 10)
    end = datetime.now()
    print("多进程&多线程耗时:{} s".format((end - start).seconds))