"""
Defines syntax objects, which contain the abstract syntax of the various types
of declarations that make up a program. Syntax objects are created by parsing
input text.

Syntax objects have two major methods: The static :meth:`~.ProgramSyntax.parse`
method constructs a new syntax object from raw input text, and
:meth:`~.ProgramSyntax.compile` constructs a new, semantically valid
declaration object.
"""
