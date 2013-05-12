'''
Defines classes for box declarations that represent macros (i.e., other
relation constraints used as boxes).
'''

from fbrelation.exceptions import ExecutionError

from fbrelation.declarations.box.base import BoxDeclaration
from fbrelation.declarations.node import MacroNodeDeclaration

class MacroBoxDeclaration(BoxDeclaration):
    '''
    Defines the declaration of a macro box, which contains a reference to the
    relation declaration to be used.
    '''

    def __init__(self, name, relationDeclaration):
        '''
        Initializes a new macro box which will create an instance of the
        specified relation constraint as a macro.
        '''
        super(MacroBoxDeclaration, self).__init__(name)
        self.relation = relationDeclaration

    def execute(self, constraint, relationComponents):
        '''
        Executes the declaration, finding the associated relation constraint
        and adding it to the provided constraint as a macro.

        :param relationComponents: Used to look up the exact name of the
                                   FBConstraintRelation that was created from
                                   the relation declaration, as the name may
                                   have been changed on creation.
        '''
        # Get the constraint from the collection of already-created relations
        assert self.relation.name in relationComponents
        macroConstraint = relationComponents[self.relation.name]

        # Create a macro box using that constraint
        box = constraint.CreateFunctionBox('My Macros',
            macroConstraint.LongName)
        assert box

        # Return the newly created box
        return box

    def createNodeDeclaration(self, nodeName, isSrc):
        '''
        Overridden to create instances of :class:`.MacroNodeDeclaration` for
        nodes that reference macro boxes.

        :note: When a macro box's node is referenced in a connection, the node
               name given corresponds to the name of input or output box in the
               original relation constraint. At runtime, these nodes are
               located by index rather than by the name of the FBAnimationNode.
        '''
        # A source node in a connection indicates a macro output; a destination
        # node indicates a macro input
        isInput = not isSrc

        # Get the index associated with the named macro tool in the associated
        # relation constraint, then use it to create a macro node declaration.
        nodeIndex = self.relation.getMacroNodeIndex(nodeName, isInput)
        assert nodeIndex >= 0, (
            'Macro nodes referenced in connection declarations must be valid.')
        return MacroNodeDeclaration(self, nodeIndex, isSrc)

    def supportsNode(self, nodeName):
        '''
        Overridden to require that the name given is a valid input or output
        box name in the associated relation constraint.
        '''
        return self.relation.hasMacroTool(nodeName)
