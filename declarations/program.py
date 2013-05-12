'''
Defines declaration classes for entire programs.
'''

class ProgramDeclaration(object):
    '''
    Defines a program declaration, which consists of a series of individual
    relation constraint declarations.
    '''

    def __init__(self, relationDeclarations):
        '''
        Initializes a new program from the provided list of relation
        constraint declaration objects.
        '''
        self.relations = relationDeclarations

    def execute(self):
        '''
        Executes the program, creating and configuring an FBConstraintRelation
        for each relation declaration in the program.

        :returns: a dictionary which maps the names of the relation
                  declarations to their corresponding constraint objects.
        :raises:  an :class:`.ExecutionError` if any problems are encountered
                  at runtime.
        '''
        # Collect a dictionary of name -> FBConstraintRelation mappings as
        # each relation is executed
        relationComponents = {}

        # Execute each individual relation declaration
        for relationDeclaration in self.relations:

            # Create the FBConstraintRelation by executing the relation,
            # passing in the dictionary of already-created relation
            # constraints. Then add the new constraint to the dictionary.
            constraint = relationDeclaration.execute(relationComponents)
            relationComponents[relationDeclaration.name] = constraint

        # Return the dictionary of relation constraints to complete the program
        return relationComponents
