fbrelation
==========

fbrelation is a simple declarative language for creating MotionBuilder relation
constraints. After writing a lot of cumbersome scripts to manipulate relation
constraints with pyfbsdk, I decided to take a stab at improving that process as
a weekend project. The resulting language takes inspiration from Graphviz DOT
and looks like this:

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

Documentation
-------------

Online documentation is available here:

-   http://awforsythe.com/fbrelation/

Full documentation is included with the source and can be built using Sphinx.

Limitations
-----------

There are a few major areas for improvement in the current implementation:

-   When the interpreter creates relation constraints, it does not arrange
    their boxes in a way that's particularly organized or aesthetically
    pleasing. Procedural layout functionality could be added, and support could
    be added for manually specifying x and y coordinates in boxes' attribute
    lists.

-   Some syntactic sugar could be added for various shortcuts in connection
    declarations. For example, it'd be handy to be able to declare a connection
    straight from a vector output to a number input, and have the interpreter
    automatically create the necessary converters, e.g.:
    `cube.Translation.X -> camera.Roll`

-   Constants can not currently be connected to input nodes, e.g.:
    `(90.0, 0.0, 0.0) -> null.Lcl Rotation`. As discussed below, the API
    doesn't support connecting constants at all, so this addition would need to
    use a sender component to contain these values as custom properties.

Additionally, some significant limitations of the MotionBuilder API prevent
this library from being very useful in production:

-   The API does not provide a means of plugging constant values into a box's
    input nodes.

-   The API does not provide a means of renaming the animation nodes of macro
    input and output boxes from the default names of "Input" and "Output".

-   Once a function box is added to a relation constraint, there's no way to
    determine the box's type or group name. This omission from the API makes it
    impossible to reliably serialize already-authored relation constraints into
    fbrelation programs, meaning that the library only works one-way.
