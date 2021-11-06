---
title: pytest for Map Reduce
categories:
- python
tags:
- map
- pytest
- reduce
date: '2021-10-31 13:14:04'
layout: post
---

### conftest.py
...
{% highlight ruby %}
@pytest.fixture
def tmp_dir():
    root_path = os.getcwd()
    letters = string.ascii_lowercase
    tmp_name = "".join(choice(letters) for _ in range(8))
    return os.path.join(root_path, tmp_name)
{% endhighlight %}
{% highlight ruby %}
@pytest.fixture
def make_test_files(tmp_dir):
    print(f"\ntest_files at {tmp_dir}")
    os.makedirs(tmp_dir, exist_ok=True)
    letters = string.ascii_lowercase
    total_count = 0
    for i in range(10):
        with open(os.path.join(tmp_dir, "{:02d}.txt".format(i)), "w") as wf:
            for j in range(randint(100, 200)):
                line: str = "".join(choice(letters) for k in range(160)) + "\n"
                total_count += 1
                wf.write(line)
    return total_count
{% endhighlight %}
{% highlight ruby %}
@pytest.fixture
def test_files_ready(request, make_test_files, tmp_dir):
    total_count = make_test_files
    def teardown_remove_temp():
        print(f"\nremove {tmp_dir}")
        remove_dir(tmp_dir)
    request.addfinalizer(teardown_remove_temp)
    return total_count
{% endhighlight %}
{% highlight ruby %}
@pytest.fixture
def elapsed_time():
    start = datetime.now()
    yield
    elapsed = datetime.now() - start
    print(f"\nruntime={elapsed.total_seconds():.3f}sec")
{% endhighlight %}
<!--more-->
### test for input data
{% highlight ruby %}
import pytest
import os
from src.mapreduce import InputData
from src.mapreduce import FileInputData
{% endhighlight %}
{% highlight ruby %}
def test_input_data_read_not_implemented_error():
    input_data = InputData()
    with pytest.raises(NotImplementedError):
        input_data.read()
{% endhighlight %}
{% highlight ruby %}
def test_input_data_generate_inputs_not_implemented_error():
    input_data = InputData()
    with pytest.raises(NotImplementedError):
        input_data.generate_inputs("path")
@pytest.mark.usefixtures("test_files_ready")
{% endhighlight %}
{% highlight ruby %}
def test_create_file_input_data_ok(tmp_dir):
    file_path = os.path.join(tmp_dir, "00.txt")
    file_input_data = FileInputData(file_path)
    assert file_input_data.path == file_path
@pytest.mark.parametrize("data_dir", ["", "file.txt"])
{% endhighlight %}
{% highlight ruby %}
def test_create_file_input_data_ng(data_dir):
    with pytest.raises(ValueError):
        FileInputData(data_dir)
{% endhighlight %}
### test for Map Reduce
{% highlight ruby %}
import pytest
from src.mapreduce import map_reduce
from src.mapreduce import FileInputData
from src.mapreduce import LineCountWorker
{% endhighlight %}
{% highlight ruby %}
def test_map_reduce_performance(elapsed_time, test_files_ready, tmp_dir):
    total_count = test_files_ready
    result = map_reduce(LineCountWorker, FileInputData, tmp_dir)
    assert result == total_count
{% endhighlight %}
