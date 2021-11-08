"""
In this problem, we have some input data stored in an XML and a JSON file,
and we want to parse them and retrieve some information. At the same time,
we want to centralize the client's connection to those (and all future)
external services. We will use the Factory Method to solve this problem.
The example focuses only on XML and JSON, but adding support for more
services should be straightforward.
"""
import xml.etree.ElementTree as etree
import json
import pytest


class JSONConnector:
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode="r", encoding="utf-8") as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


class XMLConnector:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree


def connection_factory(filepath):
    """
    Factory Method
    :param filepath: file path for json or xml
    :return: JSONConnector or XMLConnector
    """
    if filepath.endswith("json"):
        connector = JSONConnector
    elif filepath.endswith("xml"):
        connector = XMLConnector
    else:
        raise ValueError(f"Cannot connect to {filepath}")
    return connector(filepath)


def connect_to(filepath):
    """
    a wrapper of connection_factory()
    :param filepath: file path for json or xml
    :return: JSONConnector or XMLConnector
    """
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    return factory


def test_connect_to_exception_check():
    sqlite_factory = connect_to("data/person.sq3")
    assert sqlite_factory is None


@pytest.mark.parametrize("filepath", ["data/donut.json", "data/person.xml"])
def test_connect_to_ok(filepath):
    factory = connect_to(filepath)
    assert factory is not None


@pytest.mark.parametrize("filepath, size", [("data/donut.json", 3)])
def test_json_factory_ok(filepath, size):
    json_factory = connect_to(filepath)
    json_data = json_factory.parsed_data
    assert size == len(json_data)


@pytest.mark.parametrize("filepath, size", [("data/person.xml", 2)])
def test_xml_factory_ok(filepath, size):
    xml_factory = connect_to(filepath)
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//person[lastName='Liar']")
    assert isinstance(liars, object)
    assert size == len(liars)


if __name__ == "__main__":
    # check exception handling
    sqlite_factory = connect_to("data/person.sq3")
    print(sqlite_factory)
    # xml example
    xml_factory = connect_to("data/person.xml")
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//person[lastName='Liar']")
    print("found : {} persons".format(len(liars)))
    for liar in liars:
        print(f"first name: {liar.find('firstName').text}")
        print(f"last name: {liar.find('lastName').text}")
        [
            print(f"phone number ({p.attrib['type']}):", p.text)
            for p in liar.find("phoneNumbers")
        ]
    print()

    json_factory = connect_to("data/donut.json")
    json_data = json_factory.parsed_data
    print(f"found: {len(json_data)} donuts")
    for donut in json_data:
        print(f"name: {donut['name']}")
        print(f"price: ${donut['ppu']}")
        [print(f"topping: {t['id']} {t['type']}") for t in donut["topping"]]
