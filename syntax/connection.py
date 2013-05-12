'''
Defines classes for parsing and compiling connection declarations, which
consist of exactly two node declarations separated by an arrow (`->`)::

    <node> -> <node>
'''

from fbrelation.exceptions import ParsingError

from fbrelation.syntax.node import NodeSyntax

from fbrelation.declarations.connection import ConnectionDeclaration

class ConnectionSyntax(object):
    '''
    Represents the abstract syntax of a connection declaration, which consists
    of two node syntax objects. The source node conveys data (output) to the
    destination node (input).
    '''

    def __init__(self, srcNode, dstNode):
        '''
        Initializes a new connection syntax object with the given source and
        destination nodes.
        '''
        self.src = srcNode
        self.dst = dstNode

    def __str__(self):
        '''
        Converts the connection syntax back into raw text.
        '''
        return '%s -> %s' % (str(self.src), str(self.dst))

    def compile(self, boxes):
        '''
        Compiles this object into a :class:`.ConnectionDeclaration` by
        compiling the source and destination nodes in turn.

        :param boxes: The list of compiled box declarations.
        
        :returns: the newly created connection declaration.
        :raises:  a :class:`.CompilationError` if any static checks fail.
        '''
        return ConnectionDeclaration(
            self.src.compile(boxes, isSrc = True),
            self.dst.compile(boxes, isSrc = False))

    @classmethod
    def parse(cls, text):
        '''
        Parses the given input text to produce a new ConnectionSyntax object.

        :returns: the newly created syntax object.
        :raises:  a :class:`.ParsingError` if the syntax is invalid.
        '''
        # Split the input string on the arrow, which should result in a
        # two-element list containing the source node and destination node
        tokens = text.split('->')

        # Raise a syntax error if we don't have exactly two tokens
        if len(tokens) < 2 or not tokens[0] or not tokens[1]:
            raise ParsingError(
                '"%s": Incomplete connection declaration.' % text)
        elif len(tokens) > 2:
            raise ParsingError(
                '"%s": Too many nodes for a single connection declaration.' %
                text)

        # Parse the individual nodes and construct a new ConnectionSyntax
        # data structure
        srcNodeText, dstNodeText = tokens
        return cls(
            NodeSyntax.parse(srcNodeText),
            NodeSyntax.parse(dstNodeText))
