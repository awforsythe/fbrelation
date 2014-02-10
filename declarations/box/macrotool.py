"""
Defines classes for macro tools, special forms of function boxes that allow
the relation constraints in which they're included to be used as a macros.
"""

from fbrelation.declarations.box.function import FunctionBoxDeclaration
from fbrelation.declarations.node import MacroToolNodeDeclaration

class MacroToolBoxDeclaration(FunctionBoxDeclaration):
    """
    Defines the base class for a macro tool box, which may be either an input
    or an output within some relation constraint.
    """

    def createNodeDeclaration(self, nodeName, isSrc):
        """
        Overridden to use the :class:`.MacroToolNodeDeclaration` class for
        nodes that reference macro inputs or outputs.
        """
        return MacroToolNodeDeclaration(self, isSrc)

    def supportsNode(self, nodeName):
        """
        Overridden to require that no nodeName be specified in the connection
        declaration, since a macro tool has exactly one input or output node,
        which is not addressed by name.
        """
        return not nodeName

    def isMacroTool(self, isInput):
        """
        Overridden to be pure virtual, since for a generalized macro tool the
        significance of isInput can not be determined.
        """
        raise NotImplementedError

class MacroInputBoxDeclaration(MacroToolBoxDeclaration):
    """
    Defines the declaration of a macro input box, which has a single output
    node within some relation constraint.
    """

    def __init__(self, name, inputType):
        """
        Initializes a macro input box of the specified type, passing the
        appropriate group and type name to the superclass constructor.

        :param inputType: Valid built-in types are "Bool", "ColorAndAlpha",
                          "Number", "Time", and "Vector".
        """
        super(MacroInputBoxDeclaration, self).__init__(
            name,
            'Macro Tools',
            'Macro Input %s' % inputType)

    def isMacroTool(self, isInput):
        """
        Overridden to indicate that this box is an input macro tool.
        """
        return isInput

class MacroOutputBoxDeclaration(MacroToolBoxDeclaration):
    """
    Defines the declaration of a macro output box, which has a single input
    node within some relation constraint.
    """

    def __init__(self, name, outputType):
        """
        Initializes a macro output box of the specified type, passing the
        appropriate group and type name to the superclass constructor.

        :param outputType: Valid built-in types are "Bool", "ColorAndAlpha",
                           "Number", "Time", and "Vector".
        """
        super(MacroOutputBoxDeclaration, self).__init__(
            name,
            'Macro Tools',
            'Macro Output %s' % outputType)

    def isMacroTool(self, isInput):
        """
        Overridden to indicate that this box is an output macro tool.
        """
        return not isInput
