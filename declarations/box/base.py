'''
Defines base classes for box declarations.
'''

from fbrelation.declarations.node import BoxNodeDeclaration

class BoxDeclaration(object):
    '''
    An abstract base class that defines the declaration of a box within a
    relation constraint. All types of boxes can have nodes which are referenced
    by connections.
    '''
    
    def __init__(self, name):
        '''
        Initializes a new box declaration with the given name.
        '''
        self.name = name

    def execute(self, constraint, relationComponents):
        '''
        Overridden by subclasses in order to create and configure a new box of
        the appropriate type within the given FBConstraintRelation.

        :param relationComponents: Maps the names of the relation declarations
                                   executed so far to the corresponding
                                   FBConstraintRelation objects. Used to
                                   resolve macro references.

        :returns: The newly created FBBox object.
        :raises:  an :class:`.ExecutionError` if the box can not be created.
        '''
        raise NotImplementedError

    def createNodeDeclaration(self, nodeName, isSrc):
        '''
        Creates and returns a new :class:`.NodeDeclaration` object for a node
        of the given name within this box.

        :param isSrc: Represents whether the connection uses this box as a
                      source (with an output node) or a destination (with an
                      input node).

        :note: The default implementation uses the base
               :class:`.BoxNodeDeclaration` class, but subclasses may override
               this method to create more specialized node declarations.
        '''
        return BoxNodeDeclaration(self, nodeName, isSrc)

    def supportsNode(self, nodeName):
        '''
        Returns whether this box could possibly support a connection to a node
        of the given name.

        :note: A return value of True is not confirmation that the box
               absolutely will have a node of the given name in MotionBuilder,
               but it allows us to perform some rudimentary static checking at
               compile-time.
        :note: The default implementation simply requires that a non-blank node
               name be given in the node declaration.
        '''
        return bool(nodeName)

    def prepareNode(self, nodeName):
        '''
        Signals to the box declaration that a connection is about to be made
        using one of the box's nodes. Gives the box an opportunity to ensure
        that the node exists.

        :note: The default implementation does nothing, but subclasses can
               override this method as necessary.
        '''
        pass

    def isMacroTool(self, isInput):
        '''
        Returns whether this box represents either an input or an output macro
        tool, depending on the value of isInput.

        :note: The default implementation simply returns False to indicate that
               the box is not a macro tool at all.
        '''
        return False
