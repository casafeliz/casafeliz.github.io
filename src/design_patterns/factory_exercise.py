import pytest


class AutoIncreaseId:
    def __init__(self):
        self.id = 0

    def __call__(self):
        val = self.id
        self.id += 1
        return val

    def __str__(self):
        return f"{self.id}"


auto_id = AutoIncreaseId()


class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"


class PersonFactory:
    def create_person(self, name):
        return Person(auto_id(), name)


@pytest.mark.parametrize("person_list", [["John", "Smith", "Alex"]])
def test_exercise(person_list):
    p = PersonFactory()
    for idx, name in enumerate(person_list):
        person = p.create_person(name)
        assert person.name == name
        assert person.id == idx
