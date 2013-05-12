Introduction
============

- **Author:** Alex Forsythe <http://awforsythe.com>
- **Contact:** awforsythe@gmail.com
- **Download:** https://github.com/awforsythe/fbrelation

**fbrelation** is a Python library for MotionBuilder that defines a small
declarative language for creating relation constraints. The library defines
just three public symbols:

- :func:`.load`: Runs a program from an open file.
- :func:`.loads`: Runs a program from a string.
- :class:`.RelationException`: Raised in response to errors during parsing,
  compilation, or execution of a program.

Usage
=====

Here's a very basic example script. It defines a relation constraint macro that
doubles an input number::

    import fbrelation
    fbrelation.loads('''
        double_input
        {
            in [input="Number"]
            doubler [group="Number", type="Add (a + b)"]
            out [output="Number"]
            in -> doubler.a
            in -> doubler.b
            doubler.Result -> out
        }
    ''')

Here's another example that loads a program from a file and catches exceptions
as well::

    import fbrelation as rel

    def run(path):
        ''' Runs the fbrelation program located at the given file path. '''
        with open(path) as fp:
            try:
                return rel.load(fp)
            except rel.RelationException as e:
                print e

Program structure
=================

An fbrelation program consists of a series of relation constraint declarations,
each of which consists of a number of box and connection declarations. Here's a
small example program that defines a linear interpolation macro::

    linear_interpolate
    {
        # Macro input boxes
        a [input="Number"]
        b [input="Number"]
        t [input="Number"]
    
        # Operations
        sub  [group="Number", type="Subtract (a - b)"]
        mult [group="Number", type="Multiply (a x b)"]
        add  [group="Number", type="Add (a + b)"]
    
        # Macro output
        r [output="Number"]
                     
                  b -> sub.a   # b - a
                  a -> sub.b
                     
         sub.Result -> mult.a  # (b - a) * t
                  t -> mult.b
    
                  a -> add.a   # a * ((b - a) * t)
        mult.Result -> add.b
    
         add.Result -> r
    }

Line breaks are necessary to separate box and connection declarations, but
whitespace and indentation don't matter. Most characters (including
underscores, hypens, and spaces) are legal in constraint, box, and node names.

There are five kinds of box declarations: macro inputs, macro outputs, plain
function boxes, senders, and receivers. This second example demonstrates the
latter three::

    test_constraint
    {
        # Sender and receiver boxes
        null [sender="Null"]    # "Model::Null" must exist in the scene
        cube [receiver="Cube"]  # "Model::Cube" must exist in the scene

        # Ordinary function boxes
        null-translation [group="Converters", type="Vector to Number"]
        cube-translation [group="Converters", type="Number to Vector"]

        # A macro box (refers to an earlier-defined relation
        #              in the same program)
        lerp [macro="linear_interpolate"]

        null.Translation -> null-translation.V

        null-translation.X -> lerp.a
        null-translation.Y -> lerp.b
        null-translation.Z -> lerp.t

        lerp.r -> cube-translation.X
        
        cube-translation.Result -> cube.Lcl Translation
    }

Implementation details
======================

To simply use the library, :func:`.loads`, :func:`.load`, and
:class:`.RelationException` are the only public symbols you need to worry
about. If you'd like to see how the library works under the hood, though, feel
free to keep reading about :mod:`.fbrelation` and its submodules:

- :mod:`.fbrelation.__init__`: The main package.
    - :mod:`.fbrelation.syntax`: Abstract syntax. Parsing and compilation.
    - :mod:`.fbrelation.declarations`: Program semantics. Execution.
    - :mod:`.fbrelation.exceptions`: Defines exceptions.
    - :mod:`.fbrelation.utility`: Defines utility functions.

.. toctree::
   :hidden:

   fbrelation
