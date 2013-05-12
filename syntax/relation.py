'''
Defines classes for parsing and compiling relation declarations, which consist
of a name, then a series of newline-separated box and connection declarations
inside a block of curly braces. Shell-style comments (prefixed with `#`) may be
included within the body::

    name
    {
        <box|connection>
        <box|connection>
        ...
        <box|connection>
    }
'''

from fbrelation.exceptions import ParsingError

from fbrelation.syntax.box import BoxSyntax
from fbrelation.syntax.connection import ConnectionSyntax

from fbrelation.declarations.relation import RelationDeclaration

class RelationSyntax(object):
    '''
    Represents the abstract syntax of a relation constraint declaration,
    consisting of a name, a list of box syntax objects, and a list of
    connection syntax objects. Note that order is preserved among boxes and
    among connections respectively, but that the order of connections relative
    to boxes is insignificant.
    '''

    def __init__(self, name, boxes, connections):
        '''
        Initializes a new relation syntax object with the given name and the
        the provided box and connection structures.
        '''
        self.name = name
        self.boxes = boxes
        self.connections = connections

    def __str__(self):
        '''
        Converts the syntax object into its raw string representation.
        '''
        boxStrings = [str(box) for box in self.boxes]
        connectionStrings = [str(connection) for connection in self.connections]

        return '%s\n{\n    %s\n\n    %s\n}' % (
            self.name,
            '\n    '.join(boxStrings),
            '\n    '.join(connectionStrings))

    def compile(self, relations):
        '''
        Checks and compiles this relation constraint from its abstract syntax
        into a new :class:`.RelationDeclaration.` object.

        :param relations: The list of relation declarations compiled so far.
                          Used to resolve macro references.

        :returns: the newly created relation declaration.
        :raises:  a :class:`.CompilationError` if any static checks fail.
        '''
        # Compile each relation one-by-one, accumulating them into a list
        boxDeclarations = []
        for boxSyntax in self.boxes:
            box = boxSyntax.compile(boxDeclarations, relations)
            boxDeclarations.append(box)

        # With all the boxes compiled, compile all of the connections and use
        # both to construct and return a new relation declaration
        return RelationDeclaration(
            self.name,
            boxDeclarations,
            [c.compile(boxDeclarations) for c in self.connections])

    @classmethod
    def parse(cls, text):
        '''
        Parses the given input text to produce a new RelationSyntax object.

        :returns: the newly created syntax object.
        :raises:  a :class:`.ParsingError` if syntax is invalid.
        '''
        # Ensure that there are no extraneous braces to confuse things
        if text.count('{') != 1 or text.count('}') != 1:
            raise ParsingError(
                'Invalid syntax for a relation constraint declaration. '
                'Expected a single block enclosed in curly braces.')

        # Get the position of each curly brace so we can slice the input text
        openingPos = text.find('{')
        closingPos = text.find('}')

        # Slice up to the opening brace to get the name of the constraint
        name = text[:openingPos].strip()
        if not name:
            raise ParsingError(
                'Invalid syntax for a relation constraint declaration. '
                'Expected the block to be explicitly named.')

        # Collect the individual declarations (either box or connection)
        # line-by-line
        boxDeclarationsText = []
        connectionDeclarationsText = []
        for line in cls.splitBodyLines(text[openingPos+1:closingPos]):
            if '->' in line:
                connectionDeclarationsText.append(line)
            else:
                boxDeclarationsText.append(line)

        # Parse the collected input text and use the resulting data structures
        # to construct a new RelationSyntax object
        return RelationSyntax(
            name,
            [BoxSyntax.parse(t) for t in boxDeclarationsText],
            [ConnectionSyntax.parse(t) for t in connectionDeclarationsText])

    @classmethod
    def splitBodyLines(cls, text):
        '''
        Given the input text for a relation constraint definition's body,
        returns a list of the individual lines of that definition, omitting
        whitespace and comments.
        '''

        def remove_comments(line):
            '''
            Returns the given line stripped of any comments.
            '''
            hashPos = line.find('#')
            return line[:hashPos] if hashPos >= 0 else line

        # Remove comments, strip whitespace, and return only non-blank lines
        lines = map(str.strip, map(remove_comments, text.splitlines()))
        return [l for l in lines if l]
