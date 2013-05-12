fbrelation
==========

.. automodule:: fbrelation.__init__
   :members:

Running a program
=================

The implementation of :func:`.loads` shows in very clear terms what happens
when an fbrelation program is run::

    def loads(string):
        syntax = ProgramSyntax.parse(string)
        declaration = syntax.compile()
        constraints = declaration.execute()
        return constraints

First, a new :class:`.ProgramSyntax` object is constructed from the input text.
We can then use that object to compile a new :class:`.ProgramDeclaration`.
We then execute the declaration in MotionBuilder, giving us a dictionary that
contains the newly created relation constraints, indexed by name.

Elements of a program
=====================

A collection of **syntax classes** model the abstract syntax of an fbrelation
program. The syntax and structure of a program is defined recursively: a
program is made up of relations, which are made up of node and connection
declarations. The following table summarizes these composition relationships:

==============================  ==========================================  ==============================
 element                         composed of                                 syntax class
==============================  ==========================================  ==============================
:mod:`~.syntax.program`         n **relations**                             :class:`.ProgramSyntax`
:mod:`~.syntax.relation`        1 *name*, n **boxes**, m **connections**    :class:`.RelationSyntax`
:mod:`~.syntax.box`             1 *name*, 1 **attributelist**               :class:`.BoxSyntax`
:mod:`~.syntax.attributelist`   n *names*, n *values*                       :class:`.AttributeListSyntax`
:mod:`~.syntax.connection`      2 **nodes**                                 :class:`.ConnectionSyntax`
:mod:`~.syntax.node`            1 *box name*, 0 or 1 *node names*           :class:`.NodeSyntax`
==============================  ==========================================  ==============================

Once the program and its constituent elements are compiled, the program's
semantics are represented by various **declaration classes**. The syntax
objects employ an abstract factory pattern, with their compile methods creating
a declaration object of the appropriate subclass based on the details specified
in the program. The base classes for each of these elements are as follows:

======================================  ================================
 element                                 declaration class
======================================  ================================
:mod:`~.declarations.program`           :class:`.ProgramDeclaration`
:mod:`~.declarations.relation`          :class:`.RelationDeclaration`
:mod:`~.declarations.box`               :class:`.BoxDeclaration`
:mod:`~.declarations.connection`        :class:`.ConnectionDeclaration`
:mod:`~.declarations.node`              :class:`.NodeDeclaration`
======================================  ================================

Program, relation, and connection declarations do not themselves exhibit any
polymorphism, as they serve mostly as containers. The different box and node
declaration subclasses are documented in more detail in the corresponding
modules.

Package structure
=================

.. toctree::
   :maxdepth: 5

   fbrelation.syntax
   fbrelation.declarations
   fbrelation.exceptions
   fbrelation.utility
