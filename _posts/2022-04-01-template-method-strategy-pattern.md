---
title: 템플릿 메소드와 스트레티지 패턴
layout: post
date: '2022-04-01 11:27:28'
categories:
- design_pattern
---

Template Method와 Strategy Pattern은 비슷한 문제를 해결하고, 보통 호환되어 쓰인다. 
그러나 ,  **탬플릿 메소드는 문제를 해결하기 위해 상속을 사용하는 반면, 스트레티지는 위임을 사용한다.**
탬플릿 메소드와 스트레티지는 둘 다 구체적인 내용으로부터 일반적인 알고리즘을 분리하는 문제를 해결하는 패턴이다.
**의존 관계 역전을 따르기 위해서는 이 일반적인 알고리즘이 구체적 구현에 의존하지 않도록 해야 하며, 일반적인 알고리즘과 구체적인 구현이 추상화에 의존하게 해야한다.**

## 탬플릿 메소드 패턴

기본적인 메인 루프 구조
```
initialize();

while(!done())
{
    Idle();
}

cleanUp();
```

먼저, 어플리케이션을 초기화 한다.
그리고 메인 루프에 들어 간다.
메인 루프에서 프로그램이 요구하는 어떤 일을 한다.
예를 들어 GUI 이벤트를 처리하거나, 데이터 베이스 레코드를 처리할 수도 있을 것이다.
마지막으로, 모든 일이 끝나면 메인 루프를 나가면서 정리를 한다.

이 구조는 아주 평범하므로 Application이라는 이름의 클래스에 집어 넣는다.
그러고 나면 작성하려는 모든 새 프로그램에서 이 클래스를 재사용할 수 있다.

#### 화씨 온도를 섭씨 온도로 변환하는 프로그램(초기 버전)

```
def main():
    done = False

    while not done:
        print("Input Fahrenheit:")
        fahrenheit = number_from_input_stream()
        if fahrenheit is None:
            done = True
        else:
            celsius = 5.0 / 9.0 * (fahrenheit - 32)
            print(f"{fahrenheit:.2f}℉ = {celsius:.2f}℃")

    print("Fahrenheit to Celsius Finished!")
		
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def number_from_input_stream():
    parsed_number = [float(s) for s in sys.stdin.readline().split() if is_number(s)]
    if len(parsed_number) == 1:
        return parsed_number[0]
    else:
        return None
	
```

#### Application 추상 클래스

```
class Application(metaclass=ABCMeta):
    def __init__(self):
        self.done = False

    @abstractmethod
    def init(self):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def idle(self):
        raise NotImplementedError

    @abstractmethod
    def cleanup(self):
        raise NotImplementedError

    def set_done(self):
        self.done = True

    def run(self):
        self.init()
        while not self.done:
            self.idle()
        self.cleanup()
```
이 클래스는 일반적인 메인 루프 애플리케이션을 묘사하고 있다.
구현된 run 함수에서 메인 루프를 볼 수 있다.
모든 구체적인 작업이 추상 메소드인 init, idle, cleanup에 맡겨진 것 또한 볼 수 있다.
Application 을 상속하여 구현한 결과는 아래와 같다.

```
class TemperatureConverter(Application):
    def __init__(self):
        super().__init__()

    def init(self):
        self.done = False

    def idle(self):
        print("Input Fahrenheit:")
        fahrenheit = number_from_input_stream()
        if fahrenheit is None:
            self.set_done()
        else:
            celsius = 5.0 / 9.0 * (fahrenheit - 32)
            print(f"{fahrenheit:.2f}℉ = {celsius:.2f}℃")

    def cleanup(self):
        print("Fahrenheit to Celsius Finished!")


if __name__ == '__main__':
    converter = TemperatureConverter()
    converter.run()
```

이렇게 특정 애플리케이션에 탬플릿 메소드를 사용하는 것은 바람직하지 않다.
프로그램이 복잡해지고 내용만 더 늘어날 뿐이다.


템플릿 메소드 패턴은 객체 지향 프로그래밍에서 고전적인 재사용 형태 중의 하나를 보여준다.
일반적인 알고리즘은 기반 클래스에 있고, 다른 구체적인 내용에서 상속된다.
**상속은 아주 강한 관계여서, 파생 클래스는 필연적으로 기반 클래스에 묶이게 된다.**


## 스트래티지 패턴

스트래티지 패턴은 일반적인 알고리즘과 구체적인 구현 사이의 의존성 반전 문제를 완전히 다른 방식으로 풀어낸다.
앞의 탬플릿 패턴과 같이 일반적인 알고리즘을 추상 기반 클래스에 넣는 대신, ApplicationRunner라는 이름의 구체 클래스에 넣는다.
Application이란 이름의 인터페이스 안에서 일반적 알고리즘이 호출해야할 추상 메소드를 정의한다.
이 인터페이스에서 ConverterStrategy를 파생시켜 ApplicationRunner에게 넘겨 준다.
그러면 ApplicationRunner는 이 인터페이스에 위임한다.

![스트래티지]({{site.url}}/assets/img/strategy.jpg){:class="img-responsive"}

ApplicationRunner Class
```
class ApplicationRunner:
    def __init__(self, application):
        self.application = application

    def run(self):
        self.application.init()
        while not self.application.done:
            self.application.idle()
        self.application.cleanup()
```

Application Interface
```
class Application(metaclass=ABCMeta):
    @abstractmethod
    def init(self):
        raise NotImplementedError

    @abstractmethod
    def idle(self):
        raise NotImplementedError

    @abstractmethod
    def cleanup(self):
        raise NotImplementedError

    @abstractmethod
    def set_done(self):
        raise NotImplementedError
```

ConverterStrategy Class
```
class ConverterStrategy(Application):
    def __init__(self):
        self.done = False

    def init(self):
        self.done = False

    def idle(self):
        print("Input Fahrenheit:")
        fahrenheit = number_from_input_stream()
        if fahrenheit is None:
            self.set_done()
        else:
            celsius = 5.0 / 9.0 * (fahrenheit - 32)
            print(f"{fahrenheit:.2f}℉ = {celsius:.2f}℃")

    def cleanup(self):
        print("Fahrenheit to Celsius Finished!")

    def set_done(self):
        self.done = True
```
main 함수 
```
runner = ApplicationRunner(ConverterStrategy())
runner.run()
```

이 구조는 이익과 비용 면에서 템플릿 메소드 구조에 비해 더 낫다는 사실이 명백하다.
스트래티지에는 탬플릿 메소드보다 더 많은 전체 클래스 개수와 더 많은 간접 지정이 있다.
ApplicationRunner 내부의 위임 포인트는 실행 시간과 데이터 공간 면에서 상속의 경우보다 좀 더 많은 비용을 초래한다.
반면, 서로 다른 많은 애플리케이션을 실행한다면, ApplicationRunner 인스턴트를 재사용하여 Application의 다른 많은 구현에 이것을 넘겨 줄 수 있을 테고,  그럼으로써 **일반적인 알고리즘과 그성이 제어하는 구체적인 부분 사이의 결합 정도를 감소 시킬 수 있다.**


**템플릿 메소드 패턴이 일반적인 알고리즘으로 많은 구체적인 구현을 조작할 수 있게 해주는 반면, DIP를 준수하는 스트래티지 패턴은 각각의 구체적인 구현이 다른 많은 일반적인 알고리즘에 의해 조작될 수 있게 해준다.**
