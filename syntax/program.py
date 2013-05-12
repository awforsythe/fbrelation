'''
Defines classes for parsing and compiling programs, which consist of a series
of relation constraint declarations::

    <relation>
    <relation>
    ...
    <relation>
'''

import re

from fbrelation.syntax.relation import RelationSyntax

from fbrelation.declarations.program import ProgramDeclaration

class ProgramSyntax(object):
    '''
    Represents the abstract syntax of an entire program, which consists of a
    series of relation declarations.
    '''

    def __init__(self, relations):
        '''
        Initializes a new program syntax structure with the given list of
        relation syntax objects.
        '''
        self.relations = relations

    def __str__(self):
        '''
        Converts the program back into a raw string representation equivalent
        to its input text.
        '''
        relationStrings = [str(relation) for relation in self.relations]
        return '%s\n' % '\n\n'.join(relationStrings)

    def compile(self):
        '''
        Compiles the entire program from its abstract syntax structure into a
        :class:`.ProgramDeclaration`.

        :returns: the resulting program declaration.
        :raises:  a :class:`.CompilationError` if the program fails to
                  statically check.
        '''
        # Compile each relation constraint one-by-one, collecting the newly
        # created declarations into a list
        relationDeclarations = []
        for relationSyntax in self.relations:
            
            # Pass the list of previously-created relations to the new one
            relation = relationSyntax.compile(relationDeclarations)
            relationDeclarations.append(relation)

        # Construct a new program from the accumulated relation declarations
        return ProgramDeclaration(relationDeclarations)

    @classmethod
    def parse(cls, text):
        '''
        Parses the given input text to produce a new ProgramSyntax object.

        :returns: the newly created syntax structure for the entire program.
        :raises:  a :class:`.ParsingError` if the program contains any invalid
                  syntax.
        '''
        return ProgramSyntax([RelationSyntax.parse(t) for
            t in re.compile(r'.*\s*{[^{}]*}').findall(text)])
