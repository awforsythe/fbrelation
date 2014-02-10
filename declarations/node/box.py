"""
Defines classes for node declarations that represent ordinary boxes.
"""

from fbrelation.exceptions import ExecutionError

from fbrelation.declarations.node.base import NodeDeclaration

class BoxNodeDeclaration(NodeDeclaration):
    """
    Represents an animation node associated with an ordinary box.
    """

    def __init__(self, boxDeclaration, nodeName, isSrc):
        """
        Initializes a new declaration object for a box node, storing the given
        node name for use in finding the animation node within the box.
        """
        super(BoxNodeDeclaration, self).__init__(boxDeclaration, isSrc)
        self.nodeName = nodeName

    def execute(self, boxComponent):
        """
        Overridden to find the associated node by name within the given FBBox
        object.

        :returns: the FBAnimationNode that corresponds to this declaration.
        :raises:  an :class:`.ExecutionError` if no matching node is found.
        """
        self.box.prepareNode(self.nodeName)
        nodeComponent = self._findNode(boxComponent, self.nodeName)
        if not nodeComponent:
            raise ExecutionError(
                'Could not find a node named "%s" in the box named "%s".' %
                (self.nodeName, self.box.name))
        return nodeComponent
