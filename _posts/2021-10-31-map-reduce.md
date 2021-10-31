---
title: Map Reduce
layout: post
categories:
- python
date: '2021-10-31 12:56:25'
tags:
- map
---

### import library
{% highlight ruby %}
import os
from threading import Thread
{% endhighlight %}

### Input Class 선언
{% highlight ruby %}
class InputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, file_path: str):
        raise NotImplementedError


class FileInputData(InputData):
    def __init__(self, file_path):
        if not file_path:
            raise ValueError(f"path error : {file_path}")
        super().__init__()

        if not os.path.isfile(file_path):
            raise ValueError(f"file not exists {file_path}")

        self.path = file_path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, path: str):
        for name in os.listdir(path):
            yield cls(os.path.join(path, name))
{% endhighlight %}

### Worker Class 선언
{% highlight ruby %}
class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, path):
        workers = []
        for input_data in input_class.generate_inputs(path):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other):
        self.result += other.result
{% endhighlight %}

### Map Reduce 수행
{% highlight ruby %}
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)

    return first.result

def map_reduce(worker_class, input_class, path):
    workers = worker_class.create_workers(input_class, path)
    return execute(workers)

{% endhighlight %}
