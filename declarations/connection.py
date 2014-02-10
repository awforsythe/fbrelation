"""
Defines declaration classes for connections between nodes.
"""

import pyfbsdk

class ConnectionDeclaration(object):
    """
    Defines a connection declaration, which consists of two node declarations.
    The source (output) node connects to the destination (input) node.
    """

    def __init__(self, srcNodeDeclaration, dstNodeDeclaration):
        """
        Initializes the connection with the given node declaration objects.
        """
        self.src = srcNodeDeclaration
        self.dst = dstNodeDeclaration

    def execute(self, boxComponents):
        """
        Executes the connection, causing a connection to be made between the
        FBAnimationNode objects referred to in each node declaration.

        :param boxComponents: A dictionary which maps the names of
                              already-compiled box declarations to their
                              corresponding FBBox objects.

        :returns: nothing, as there is no corresponding MotionBuilder object
                  which represents a connection.
        :raises:  an :class:`.ExecutionError` if the nodes could not be
                  executed.
        """
        # Find the actual FBBoxes which contain the nodes to connect
        srcBoxComponent = boxComponents[self.src.box.name]
        dstBoxComponent = boxComponents[self.dst.box.name]

        # Execute each node to obtain the FBAnimationNodes from those boxes
        srcNode = self.src.execute(srcBoxComponent)
        dstNode = self.dst.execute(dstBoxComponent)

        # Connect the two nodes in order to execute the connection
        pyfbsdk.FBConnect(srcNode, dstNode)
