'''
`fbrelation.exceptions`

Defines exception classes used by the library.
'''

class RelationException(Exception):
    '''
    Base class for all exceptions relating to relation constraint declarations.
    '''
    pass

class ParsingError(RelationException):
    '''
    Indicates a problem with the syntax of a declaration (improper formatting,
    for example). May be raised during parsing, when the input text is being
    parsed into abstract syntax objects.
    '''
    pass

class CompilationError(RelationException):
    '''
    Indicates a problem with the semantics of the declaration (e.g., an
    unresolved reference or an improper combination of attributes). May be
    raised during the static checking  and compilation process, when
    declaration objects are being built from abstract syntax data structures.
    '''
    pass

class ExecutionError(RelationException):
    '''
    Indicates a runtime problem that could not be anticipated through static
    checking, such as a missing animation node, component, or function box
    type within MotionBuilder. May be raised during execution, when
    FBConstraintRelation objects are being instantiated from declarations.
    '''
    pass
