'''
Defines declaration objects, which represent compiled, semantically validated
expressions within a program. Declarations are created from the corresponding
syntax objects by calling their :meth:`~.ProgramSyntax.compile` method.

All declaration objects have an :meth:`~.ProgramDeclaration.execute` method,
which attempts to construct and configure the corresponding MotionBuilder
objects based on the details of the declaration.
'''
