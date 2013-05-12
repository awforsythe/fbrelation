'''
Defines base classes for box declarations that represent function boxes.
'''

from fbrelation.exceptions import ExecutionError

from fbrelation.declarations.box.base import BoxDeclaration

class FunctionBoxDeclaration(BoxDeclaration):
    '''
    Base class for function boxes, which are created from a pool of box types
    types organized into groups. Group and box type names can not be know until
    runtime, nor can the names of the nodes of any given box type.
    '''

    def __init__(self, name, groupName, typeName):
        '''
        Initializes a new function box declaration representing a instance of
        the given box type from the given group.
        '''
        super(FunctionBoxDeclaration, self).__init__(name)
        self.groupName = groupName
        self.typeName = typeName

    def execute(self, constraint, relationComponents):
        '''
        Executes the box declaration by creating function box of the
        appropriate type in the given constraint.

        :returns: the newly created FBBox.
        :raises:  an :class:`.ExecutionError` if MotionBuilder does not
                  recognize the group or type name.
        '''
        box = constraint.CreateFunctionBox(self.groupName, self.typeName)
        if not box:
            raise ExecutionError(
                'Could not create a "%s" function box from the group "%s".' %
                (self.typeName, self.groupName))
        return box
