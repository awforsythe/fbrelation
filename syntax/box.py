'''
Defines classes for parsing and compiling box declarations, which consist of a
name followed by an attribute list in square brackets. Box declarations must
occupy a single line and must not contain arrows (`->`)::

    <name> [<attributelist>]
'''

import re

from fbrelation.utility import find

from fbrelation.exceptions import ParsingError, CompilationError

from fbrelation.syntax.attributelist import AttributeListSyntax

from fbrelation.declarations.box import FunctionBoxDeclaration, \
                                        MacroInputBoxDeclaration, \
                                        MacroOutputBoxDeclaration, \
                                        MacroBoxDeclaration, \
                                        SenderBoxDeclaration, \
                                        ReceiverBoxDeclaration

class BoxSyntax(object):
    '''
    Represents the abstract syntax of a box declaration, which has a name and
    an attribute list.
    '''

    def __init__(self, name, attributeList):
        '''
        Initializes a new box syntax object with the given name and attribute
        list.
        '''
        self.name = name
        self.attributes = attributeList

    def __getitem__(self, key):
        '''
        Allows the use of square-bracket notation to retrieve the value of
        one of this box's attributes.
        '''
        return self.attributes[key]

    def __str__(self):
        '''
        Converts the syntax object into its raw string representation.
        '''
        return '%s [%s]' % (self.name, str(self.attributes))

    def compile(self, boxes, relations):
        '''
        Checks and compiles the abstract syntax structure to create a new
        :class:`.BoxDeclaration` object of the appropriate subclass.

        :param boxes: The list of box declarations compiled so far.
        :param relations: The list of relation declarations compiled so far.

        :returns: the newly created box declaration.
        :raises:  a :class:`.CompilationError` if any static checks fail.
        '''
        # Ensure that the box name is not a duplicate
        if find(lambda b: b.name == self.name, boxes):
            raise CompilationError(
                '"%s": A box by the name of "%s" already exists.' %
                (str(self), self.name))

        # Declare a helper function to determine whether an attribute has
        # been included
        includes = lambda s: s in self.attributes and self.attributes[s]

        # For a plain function box, ensure that both group name and box typ
        # name are included
        if ((includes('group') and not includes('type')) or
            (includes('type') and not includes('group'))):
            raise CompilationError(
                '"%s": Function boxes must have both group and type specified '
                'as attributes.' % str(self))

        # Check the attributes to determine which type of box this might be
        isFunction = includes('group') and includes('type')
        isMacroInput = includes('input')
        isMacroOutput = includes('output')
        isMacro = includes('macro')
        isSender = includes('sender')
        isReceiver = includes('receiver')

        # Declare helpers to check how many of these conditions is True
        count_true = lambda xs: reduce(
            lambda acc, x: acc + 1 if x else acc, xs, 0)
        exactly_one = lambda xs: count_true(xs) == 1

        # Ensure that exactly one of these cases is true: no more, no less
        if not exactly_one((isFunction, isMacroInput, isMacroOutput,
            isMacro, isSender, isReceiver)):
            raise CompilationError(
                '"%s": Invalid combination of attributes for a box '
                'declaration.' % str(self))

        # Finally, create a box declaration of the appropriate class
        if isFunction:
            return FunctionBoxDeclaration(
                self.name, self['group'], self['type'])
        if isMacroInput:
            return MacroInputBoxDeclaration(self.name, self['input'])
        if isMacroOutput:
            return MacroOutputBoxDeclaration(self.name, self['output'])
        if isMacro:
            # Require that the given macro name matches an existing relation
            relation = find(lambda r: r.name == self['macro'], relations)
            if not relation:
                raise CompilationError(
                    '"%s": No relation constraint named "%s" yet exists.' %
                    (str(self), self['macro']))
            return MacroBoxDeclaration(self.name, relation)
        if isSender:
            return SenderBoxDeclaration(self.name, self['sender'])
        if isReceiver:
            return ReceiverBoxDeclaration(self.name, self['receiver'])
        
        # We should never reach this point
        assert False

    @classmethod
    def parse(cls, text):
        '''
        Parses the given input text to produce a new BoxSyntax object.

        :returns: the newly created box syntax object.
        :raises:  a :class:`.ParsingError` if syntax is invalid.
        '''
        # Ensure that there are no extraneous brackets to confuse the regex
        if text.count('[') != 1 or text.count(']') != 1:
            raise ParsingError(
                '"%s": Invalid syntax for a box declaration. Expected a '
                'single attribute block enclosed in square brackets.' % text)

        # Match the line against a regular expression, capturing the box name
        # and the contents of the attribute list within the square brackets
        match = re.match(r'([^\[\]]*)\[([^\[\]]*)\]', text)
        if not match:
            raise ParsingError(
                '"%s": Invalid syntax for a box declaration. Expected box '
                'name followed by an attribute block.' % text)
        name, attributeText = match.groups()

        # Parse the attribute list and create a new BoxSyntax object
        return cls(name.strip(), AttributeListSyntax.parse(attributeText))
