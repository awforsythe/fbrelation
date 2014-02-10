"""
**fbrelation**
    by Alex Forsythe <awforsythe@gmail.com> <http://awforsythe.com>

Defines an interpreter for a small declarative language used to define
MotionBuilder relation constraints. In this language, a program consists of a
series of relation constraint declarations, each of which contains a series
of box and connection declarations, each on its own line.

Loading a relation constraint program takes place in three phases: parsing,
compilation, and execution.

1. The **parsing** phase constructs abstract syntax objects from input text,
   using the static :meth:`~.ProgramSyntax.parse` method of the various classes
   in the syntax submodule. These methods may throw a :class:`.ParsingError` if
   they encounter malformed syntax.

2. The **compilation** phase turns abstract syntax objects into semantically
   validated declaration objects, using the :meth:`~.ProgramSyntax.compile`
   method of the individual syntax objects. These methods perform some static
   checking to ensure that the program is relatively sound. If any of these
   checks fail, a :class:`.CompilationError` will be thrown.

3. Finally, the **execution** phase constructs and configures new
   FBConstraintRelation objects from the compiled declarations. The
   :meth:`~.ProgramDeclaration.execute` methods of the declaration objects
   handle the instantiation and configuration of MotionBuilder objects, and
   they will throw an :class:`.ExecutionError` if they encounter problems at
   runtime.
"""

from fbrelation.exceptions import RelationException

from fbrelation.syntax.program import ProgramSyntax as _ProgramSyntax

def loads(string):
    """
    Parses, compiles, and executes a program from its provided source text.

    :returns: a dictionary mapping constraint declaration names to their
              corresponding FBConstraintRelation objects.
    :raises:  a :class:`.RelationException` if a program is invalid or
              unsupported.
    """
    syntax = _ProgramSyntax.parse(string)
    declaration = syntax.compile()
    return declaration.execute()

def load(fp):
    """
    Parses, compiles, and executes a program from the provided open file.

    :note:    Returns and raises identically to loads.
    """
    return loads(fp.read())
