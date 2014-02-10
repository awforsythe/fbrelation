"""
Defines declaration classes for individual relation constraints within a
program.
"""

import pyfbsdk

class RelationDeclaration(object):
    """
    Represents a parsed and statically-checked relation constraint declaration.
    Consists of a name, a series of box declarations, and a series of
    connection declarations.
    """

    def __init__(self, name, boxDeclarations, connectionDeclarations):
        """
        Initializes a new relation declaration with the given name, using the
        provided box and connection declarations.
        """
        self.name = name
        self.boxes = boxDeclarations
        self.connections = connectionDeclarations

    def execute(self, relationComponents):
        """
        Executes the relation declaration, attempting to construct and
        configure an FBConstraintRelation object in the MotionBuilder scene.

        :param relationComponents: Maps the names of the relation declarations
                                   compiled so far to their corresponding
                                   FBConstraintRelation objects.

        :returns: the newly created (and activated) FBConstraintRelation.
        :raises:  an :class:`.ExecutionError` if any box or connection
                  declarations can not be executed.
        """
        # Create an actual relation constraint in the scene
        constraint = pyfbsdk.FBConstraintRelation(self.name)
        x, y = (0, 0)

        # Collect a mapping of box names to FBBox objects as boxes are executed
        boxComponents = {}

        # Create all boxes in the order in which they were declared
        for boxDeclaration in self.boxes:

            # Execute the box declaration to create the actual FBBox object
            # within the newly created FBConstraintRelation, passing in the
            # collection of already-created relation constraints in order to
            # resolve macro references.
            box = boxDeclaration.execute(constraint, relationComponents)
            constraint.SetBoxPosition(box, x, y); x += 250; y += 100
            boxComponents[boxDeclaration.name] = box

        # With all the boxes created, execute all connections in the order in
        # which they were declared
        for connection in self.connections:
            connection.execute(boxComponents)

        # With the constraint fully configured, activate it and return it
        constraint.Active = True
        return constraint

    def hasMacroTool(self, name):
        """
        Returns whether the relation contains a macro input or output box with
        the specified name.
        """
        for box in self.boxes:
            if box.name == name:
                return box.supportsNode('')
        return False

    def getMacroNodeIndex(self, nodeName, isInput):
        """
        Returns the index associated with the macro input or output box with
        the given name. For example, if this relation includes three input
        nodes, a, b, and c, then `getMacroNodeIndex('c', True)` will return 2.
        Returns -1 if no matching macro tool can be found.
        """
        currentIndex = -1
        for box in self.boxes:
            if box.isMacroTool(isInput):
                currentIndex += 1
                if box.name == nodeName:
                    return currentIndex
        return -1
