---
title: Active Object Pattern
layout: post
categories:
- design_pattern
date: '2022-03-31 20:17:31'
---

ActiveObject 객체는 Command 객체의 리스트를 유지한다.
사용자는 ActiveObject에 새로운 명령을 추가할 수도 있고, run()을 호출할 수 도 있다.
run()은 단순히 각 명령을 실행하고 제거하면서 리스트를 훑어 나가는 함수다.

* ActiveObject

```
class ActiveObject:
    def __init__(self):
        self.command_queue = []

    def add_command(self, command):
        self.command_queue.append(command)

    def run(self):
        while len(self.command_queue):
            command = self.command_queue.pop(0)
            command.execute()						
```

* Command Interface

```
class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        raise NotImplementedError				
```

이것은 그다지 특별해 보이지 않는다.
하지만 리스트에 있는 Command 객체 중 하나가 자기를 복제하여 그 복제본을 리스트에 다시 넣는다면 어떤 일이 일어날까?
이 리스트는 절대 비지 않게되고 run()함수는 절대로 return하지 않을 것이다.

* SleepCommand

```
class SleepCommand(Command):
    def __init__(self, milliseconds, active_object, wakeup_command):
        self.start_time = 0
        self.sleep_time = milliseconds
        self.active_object = active_object
        self.wakeup_command = wakeup_command
        self.started = False

    def execute(self):
        current_time = current_time_milliseconds()
        if not self.started:
            self.started = True
            self.start_time = current_time
            self.active_object.add_command(self)
        elif (current_time - self.start_time) < self.sleep_time:
            self.active_object.add_command(self)
        else:
            self.active_object.add_command(self.wakeup_command)
```

* WakeupCommand

```
class WakeupCommand(Command):
    def execute(self):
        print("Command Executed!")
```

* TestSleepCommand

SleepCommand의 생성자는 3개의 인자를 갖는다.
첫 번째는 ms 단위의 지연 시간이다. 
두 번째는 이명령이 실행될 장소인 ActiveObject이다.
마지막 인자는 wakeup이라는 또 다른 명령 객체이다.
이 테스트가 기대하는 동작은 SleepCommand가 일정 시간만큼 기다렸다가 wakeup 명령을 실행하는 것이다.

```
class TestSleepCommand(TestCase):
    def setUp(self) -> None:
        self.active_object = ActiveObject()
        self.sleep_command = SleepCommand(1000, self.active_object, WakeupCommand())
        self.active_object.add_command(self.sleep_command)

    def test_execute(self):
        expected = "Command Executed!\n"
        buf = io.StringIO()

        start_time = current_time_milliseconds()
        with contextlib.redirect_stdout(buf):
            self.active_object.run()
        sleep_time = current_time_milliseconds() - start_time

        self.assertTrue(sleep_time >= 1000)
        self.assertTrue(sleep_time < 1100)
        self.assertEqual(expected, buf.getvalue())
```

이 기법의 다양한 변형을 사용하여 멀티스레드 시스템을 구축하는 것은, 지금까지도 그래왔고 앞으로도 계속될 아주 일반적인 실천 방법이다.
이런 종류의 스레드는 각 Command 인스턴트가 다음 Command 인스턴트 실행이 가능해지기 전에 완료되기 때문에, RTC(run-to-completion) 테스크라는 이름으로 알려져 있다.
Command인스턴트가 모두 완료될 때까지 실행된다는 사실은 RTC 스레드에 모두 같은 런타임 스택을 공유한다는 흥미로운 이점을 부여한다.
전통적인 멀티스레드 시스템에서의 스레드와 달리 여기서는 각 RTC 스레드에 대해 별도의 런타임 스택을 정의하거나 할당할 필요가 없다.
이것은 많은 스레드가 실행되고 메모리가 제한된 시스템에서 강력한 이점이 될 수 있다.
