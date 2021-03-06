from abc import ABCMeta
from cloudshell.shell.core.driver_context import AutoLoadResource, AutoLoadAttribute
from bp_chassis.autoload.model.structure_node import StructureNode


class Attribute(object):
    def __init__(self, relative_address, attribute_name, attribute_value):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self._relative_address = relative_address

    @property
    def relative_address(self):
        return self._relative_address.value

    def autoload_attribute(self):
        return AutoLoadAttribute(self._relative_address.value, self.attribute_name, self.attribute_value)


class Resource(StructureNode):
    MODEL = 'Generic resource'
    NAME_TEMPLATE = 'Resource {}'
    PREFIX = 'R'

    __metaclass__ = ABCMeta

    def __init__(self, resource_id, unique_identifier):
        StructureNode.__init__(self, resource_id)
        if unique_identifier:
            self._unique_identifier = str(unique_identifier)
        self._attributes = {}

    @property
    def autoload_attributes(self):
        autoload_attributes = []
        for attribute in self._attributes.values():
            autoload_attributes.append(attribute.autoload_attribute())
        return autoload_attributes

    @property
    def _prefix(self):
        return self.PREFIX

    @property
    def model(self):
        return self.MODEL

    @property
    def name(self):
        return self.NAME_TEMPLATE.format(self._relative_address.path_id)

    @property
    def unique_identifier(self):
        return self._unique_identifier

    def _add_attribute(self, name, value):
        attribute = Attribute(self._relative_address, name, str(value))
        self._attributes[name] = attribute

    def _get_attribute(self, name):
        return self._attributes[name].attribute_value

    def autoload_resource(self):
        return AutoLoadResource(self.model, self.name, self.relative_address, self.unique_identifier)
