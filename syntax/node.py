"""
Defines classes for parsing and compiling node declarations, which consist of
either a plain box name (indicating a macro input or output) or a box name and
node name separated by a dot::

    <boxname.nodename|boxname>
"""

from fbrelation.utility import find

from fbrelation.exceptions import ParsingError, CompilationError

class NodeSyntax(object):
    """
    Represents the abstract syntax for an animation node reference within a
    connection declaration. Consists of a box name and an optional node name to
    clarify which of the box's nodes is involved in the connection. If the node
    name is blank, it is assumed that the box name by itself is sufficient to
    deduce the node, as in the case of a macro input or output box.
    """

    def __init__(self, boxName, nodeName):
        """
        Initializes a new node syntax object to refer to some optionally named
        node in a box with the given name.
        """
        self.boxName = boxName
        self.nodeName = nodeName

    def __str__(self):
        """
        Converts the syntax object into its raw string representation.
        """
        if self.nodeName:
            return '%s.%s' % (self.boxName, self.nodeName)
        return self.boxName

    def compile(self, boxes, isSrc):
        """
        Compiles this node syntax structure into a :class:`.NodeDeclaration`
        object as either a source or a destination node.

        :param boxes: The list of compiled box declarations.
        :param isSrc: If True, the node is a source node (i.e., on the left
                      side of the arrow in the connection declaration).

        :returns: The newly created node declaration.
        :raises:  a :class:`.CompilationError` if any static checks fail.
        """
        # Find the box declaration object that owns the node in question
        box = find(lambda b: b.name == self.boxName, boxes)
        if not box:
            raise CompilationError(
                '"%s" is not a valid box name.' % self.boxName)

        # Ensure that the given box will compile with a node of the given name
        if not box.supportsNode(self.nodeName):
            raise CompilationError(
                '"%s" is not a valid node name for the box named "%s".' %
                (self.nodeName, self.boxName))

        # Finally, create and return node declaration of the appropriate type
        # based upon the type of box it belongs to
        return box.createNodeDeclaration(self.nodeName, isSrc)

    @classmethod
    def parse(cls, text):
        """
        Parses the given input text to produce a new NodeSyntax object.

        :returns: the newly created syntax object.
        :raises:  a :class:`.ParsingError` if the syntax is invalid.
        """
        # If we're given a non-dotted string, treat it as a macro input or
        # output box with no explicitly specified node name
        if '.' not in text:
            return cls(text.strip(), '')

        # Otherwise, split the string on the dot, which should result in a
        # list with exactly two elements
        tokens = text.split('.')
        if len(tokens) != 2 or not tokens[0] or not tokens[1]:
            raise ParsingError(
                '"%s": Invalid syntax for a connection declaration. Expected '
                'box name dot attribute name.' % text.strip())

        # Construct a new NodeSyntax object from the pair
        boxName, nodeName = tokens
        return cls(boxName.strip(), nodeName.strip())
