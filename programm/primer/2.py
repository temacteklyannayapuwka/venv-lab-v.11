#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Пример работы с Event-объектом

from threading import Thread, Event
from time import sleep, time

event = Event()


def worker(name: str):
    event.wait()
    print(f"Worker: {name}")


if __name__ == "__main__":
    # Clear event
    event.clear()
    # Create and start workers
    workers = [Thread(target=worker, args=(f"wrk {i}",)) for i in range(5)]
    for w in workers:
        w.start()
    print("Main thread")
    event.set()