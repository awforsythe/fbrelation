"""
Defines classes for parsing attribute lists, which are comma-separated
key/value pairs, with values in double quotes and preceded by the equals sign::

    <name>="<value>", <name>="<value>", ..., <name>="<value>"
"""

import re

from fbrelation.exceptions import ParsingError

class AttributeListSyntax(object):
    """
    Represents the abstract syntax of an attribute list, consisting of a
    collection of named attributes with associated values. Implements container
    semantics (via `in` and `[]`) to allow easy access to these key-value
    mappings.
    """

    def __init__(self, attributes):
        """
        Initializes a new attribute list syntax object with the given
        dictionary of attribute-name-to-attribute-value mappings.
        """
        self.attributes = attributes

    def __contains__(self, key):
        """
        Allows the use of the `in` keyword to determine whether an attribute
        with the given name is present in the list.
        """
        return key in self.attributes

    def __getitem__(self, key):
        """
        Allows the use of square-bracket notation to retrieve the value
        associated with a specified attribute.
        """
        return self.attributes[key]

    def __str__(self):
        """
        Converts the syntax object back to text.
        """
        return ', '.join(
            ['%s="%s"' % (key, self[key]) for key in sorted(self.attributes)])

    @classmethod
    def parse(cls, text):
        """
        Parses the given input text to produce a new AttributeListSyntax object.

        :returns: the newly created attribute list structure.
        :raises:  a :class:`.ParsingError` if the syntax is invalid.
        """
        # Parse the attribute mappings and collect them into a dictionary
        attributes = {}
        for mapping in text.split(','):

            # Match each attribute mapping against a regular expression,
            # capturing the attribute's name and value
            match = re.match(r'([^="]*)=\s*"([^"]*)"', mapping)
            if not match:
                raise ParsingError(
                    '"%s": Invalid syntax for a box attribute mapping.' % text)
            name, value = match.groups()

            # Ensure that attribute names aren't duplicated
            if name in attributes:
                raise ParsingError(
                    '"%s": Attribute name "%s" is used more than once.' %
                    (text, name))

            # Add the attribute mapping to the dictionary
            attributes[name.strip()] = value.strip()

        # Construct a new AttributeListSyntax object from the dictionary of
        # attribute -> value mappings
        return cls(attributes)
