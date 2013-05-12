'''
Defines base classes for node declarations.
'''

from fbrelation.utility import find

class NodeDeclaration(object):
    '''
    Abstract base class for a node declaration, which refers to some animation
    node of a specific box. A node declaration is one part of a connection
    declaration and is either a source (to the left of the arrow) or a
    destination (to the right of the arrow).
    '''

    def __init__(self, boxDeclaration, isSrc):
        '''
        Initializes a new node declaration which refers to some node of the
        given box. isSrc indicates whether that box is used as a source or a
        destination in the connection.
        '''
        self.box = boxDeclaration
        self.isSrc = isSrc

    def execute(self, boxComponent):
        '''
        Overridden by subclasses in order to resolve the appropriate
        FBAnimationNode of the associated box, using the supplied FBBox
        component to locate and return the node.

        :returns: the FBAnimationNode that corresponds to this declaration.
        :raises:  an :class:`.ExecutionError` if the node can not be found.
        '''
        raise NotImplementedError

    def _getParentNode(self, boxComponent):
        '''
        Helper function that returns the parent animation node on either side
        of the given box component, depending on whether the node is the source
        or the destination in its connection. Source connections send data
        through their output nodes, whereas destination connections receive
        data through their input nodes.
        '''
        if self.isSrc:
            return boxComponent.AnimationNodeOutGet()
        return boxComponent.AnimationNodeInGet()

    def _findNode(self, boxComponent, nodeName):
        '''
        Helper function that attempts to find an animation node matching the
        given name on the appropriate side (output vs. input) of the given
        FBBox object. Returns None if the box has no matching node.
        '''
        return find(lambda n: n.Name == nodeName,
            self._getParentNode(boxComponent).Nodes)

    def _getNode(self, boxComponent, nodeIndex):
        '''
        Helper function that attempts to get the animation node at the
        specified offset on the appropriate side (output vs. input) of the
        given FBBox object. Returns None if the given index is out of bounds.
        '''
        try:
            return self._getParentNode(boxComponent).Nodes[nodeIndex]
        except IndexError:
            return None
