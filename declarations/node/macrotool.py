"""
Defines classes for node declarations that relate to macro tools. Macro tools
are the input or output boxes which allow a relation to be used as a macro.
"""

from fbrelation.declarations.node.base import NodeDeclaration

class MacroToolNodeDeclaration(NodeDeclaration):
    """
    Represents a macro input or output as referenced in a connection
    declaration. A macro tool has exactly one node, so it requires no name or
    index in order to resolve that node from the associated FBBox.
    """

    def execute(self, boxComponent):
        """
        Overridden to simply use the first and only animation node on the
        appropriate side (input vs. output) of the given FBBox object.
        """
        try:
            node = self._getParentNode(boxComponent).Nodes[0]
        except IndexError:
            assert False, (
                'Macro tool boxes must have exactly one input or output node.')
        
        return node
