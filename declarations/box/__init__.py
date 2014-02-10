"""
Defines classes for the different types of box declarations.
"""

from fbrelation.declarations.box.function    import FunctionBoxDeclaration
from fbrelation.declarations.box.macrotool   import MacroInputBoxDeclaration, \
                                                    MacroOutputBoxDeclaration
from fbrelation.declarations.box.macro       import MacroBoxDeclaration
from fbrelation.declarations.box.placeholder import SenderBoxDeclaration, \
                                                    ReceiverBoxDeclaration
