---
title: List Comprehension
layout: post
date: '2021-10-29 23:52:29 +0900'
categories:
- ''
- python
---

| ![Lucky]({{site.url}}/assets/img/lucky01.jpg){:class="img-responsive"} |
|:--:|
| 한 밤에 중앙 공원에서 ...(럭키의 하루!) |

### map과 filter 대신에 리스트 컴프리헨션을 사용하자
#### 리스트 a에 있는 각 숫자의 제곱을 계산할 경우
{% highlight ruby %}
a = [1,2,3,4,5,6,7,8,9,10]
squares = [x**2 for x in a]
print(squares)
=> [1,4,9,16,25,36,49,64,81,100]
{% endhighlight %}
#### map을 사용하면 lambda가 필요해서 복잡해 진다
{% highlight ruby %}
square = map(lamda x: x**2, a)
{% endhighlight %}
### a 배열에서 2로 나누어 떨어지는 숫자만 제곱하는 경우
{% highlight ruby %}
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)
=> [4, 16, 36, 64, 100]
{% endhighlight %}
### 내장 함수 filter를 map과 함께 사용하는 경우
{% highlight ruby %}
even_squares_alt = map(lambda x: x**2, filter(labmda x: x % 2 == 0, a))
assert (even_squares == list(even_squares_alt) 
{% endhighlight %}
### 딕셔너리와 세트에도 리스트 컴프리헨션에 해당하는 문법이 있다.
{% highlight ruby %}
chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne':3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}
print(rank_dict)
print(chile_len_set)
=> {1: 'ghost', 2: 'habanero', 3: 'cayenne'}
=> {8, 5, 7}
{% endhighlight %}

[home](/)