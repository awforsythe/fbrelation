'''
Defines classes for node declarations that represent macros, or references to
earlier-defined relation constraints used as boxes.
'''

from fbrelation.exceptions import ExecutionError

from fbrelation.declarations.node.base import NodeDeclaration

class MacroNodeDeclaration(NodeDeclaration):
    '''
    Represents an input or output node of a macro box. Macro nodes employ an
    additional level of indirection over plain box nodes, as the node names
    given in the connection declarations correspond to the names of input or
    output macro tool boxes in the relation constraint instantiated by the
    macro box.
    '''

    def __init__(self, boxDeclaration, nodeIndex, isSrc):
        '''
        Initializes a new macro box node, storing the index of the node on the
        appropriate side of the corresponding macro box.
        '''
        super(MacroNodeDeclaration, self).__init__(boxDeclaration, isSrc)
        self.nodeIndex = nodeIndex

    def execute(self, boxComponent):
        '''
        Overridden to search the given FBBox object for an input or output
        animation node at the appropriate offset.

        :returns: the corresponding FBAnimationNode.
        :raises:  an :class:`.ExecutionError` if no such node can be found.
        '''
        nodeComponent = self._getNode(boxComponent, self.nodeIndex)
        if not nodeComponent:
            raise ExecutionError(
                'Macro box "%s" has no %s node at offset %d.' % (
                    self.box.name,
                    'output' if self.isSrc else 'input',
                    self.nodeIndex))
        return nodeComponent
