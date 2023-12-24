#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# В этом примере мы создаем функцию order_processor, которая может реализовывать в себе бизнес логику, например,
# обработку заказа. При этом, если она получает сообщение stop, то прекращает свое выполнение. В главном потоке мы
# создаем и запускаем три потока для обработки заказов. Запущенные потоки видят, что очередь пуста и “встают на
# блокировку” при вызове wait(). В главном потоке в очередь добавляются десять заказов и сообщения для остановки
# обработчиков, после этого вызывается метод notify_all() для оповещения всех заблокированных потоков о том, что
# данные для обработки есть в очереди.

from threading import Condition, Thread
from queue import Queue
from time import sleep

cv = Condition()
q = Queue()
# Consumer function for order processing
def order_processor(name):
    while True:
        with cv:
            # Wait while queue is empty
            while q.empty():
                cv.wait()
            try:
                # Get data (order) from queue
                order = q.get_nowait()
                print(f"{name}: {order}")
                # If get "stop" message then stop thread
                if order == "stop":
                    break
            except:
                pass
            sleep(0.1)


if __name__ == "__main__":
    # Run order processors
    Thread(target=order_processor, args=("thread 1",)).start()
    Thread(target=order_processor, args=("thread 2",)).start()
    Thread(target=order_processor, args=("thread 3",)).start()

    # Put data into queue
    for i in range(10):
        q.put(f"order {i}")

    # Put stop-commands for consumers
    for _ in range(3):
        q.put("stop")

    # Notify all consumers
    with cv:
        cv.notify_all()