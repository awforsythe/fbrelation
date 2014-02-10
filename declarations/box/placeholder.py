"""
Defines classes for placeholder boxes, which serve as proxies for scene objects
in order to send data to or receive data from the relation constraint in which
they're included.
"""

import pyfbsdk

from fbrelation.exceptions import ExecutionError

from fbrelation.declarations.box.base import BoxDeclaration

class PlaceholderBoxDeclaration(BoxDeclaration):
    """
    Defines the base class for placeholder box declarations, which include the
    name of a scene object that the declaration will attempt to locate at
    runtime.
    """

    class TransformationType(object):
        """
        Defines the space in which the placeholder box's transformations are
        expressed, if any.

        :note: If transformation nodes (either global or local translation,
               rotation, and scaling) are used in node declarations for a box,
               all such nodes must be in the same space (global vs. local) for
               the box to compile.
        """
        kNone = 0 
        """ Indicates that no transformation nodes are referenced. """

        kGlobal = 1
        """ Indicates that global transformations are to be used. """

        kLocal = 2
        """ Indicates that local transformations are to be used. """

    def __init__(self, name, componentName):
        """
        Initializes a new placeholder box declaration with the given component
        name.

        :param componentName: The full name of a scene object, in the form
                              `group::namespace:name`. If no group name is
                              specified, the name is assumed to refer to a
                              model.
        """
        super(PlaceholderBoxDeclaration, self).__init__(name)
        self.componentName = componentName
        self.transformation = self.TransformationType.kNone

    def supportsNode(self, nodeName):
        """
        Overridden to ensure that transformation nodes are either all global or
        all local, for cases in which the box is a placeholder for a model.
        """
        # If the node name is totally invalid to begin with, it's moot
        if not super(PlaceholderBoxDeclaration, self).supportsNode(nodeName):
            return False

        # Otherwise, check whether the provided node name is a transformation
        isGlobal = (nodeName == 'Translation' or
            nodeName == 'Rotation' or nodeName == 'Scaling')

        isLocal = (nodeName == 'Lcl Translation' or
            nodeName == 'Lcl Rotation' or nodeName == 'Lcl Scaling')

        # If it's not a transformation, it's supported outright
        if not (isGlobal or isLocal):
            return True

        # If it is a transformation, we need to ensure that it's not of a
        # different type (global vs. local) than any previously encountered
        # transformation node
        assert isGlobal ^ isLocal
        if ((isGlobal and
                self.transformation == self.TransformationType.kLocal) or
                (isLocal and
                self.transformation == self.TransformationType.kGlobal)):
            return False

        # If the transformation type is consistent with what we've seen so far,
        # we just need to remember that type and return True to accept the name
        if isGlobal:
            self.transformation = self.TransformationType.kGlobal
        else:
            self.transformation = self.TransformationType.kLocal
        return True

    def prepareNode(self, nodeName):
        """
        Overridden to ensure that the node with the given name exists if it
        corresponds to an animatable property.
        """
        # Get a reference to the actual component in the scene
        component = self._findComponent()
        assert component

        # Set the associated property to animated, if one can be found
        prop = component.PropertyList.Find(nodeName)
        if prop and prop.IsAnimatable() and not prop.IsAnimated():
            prop.SetAnimated(True)

    def _findComponent(self):
        """
        Attempts to find the associated scene component based on the name given
        in the box declaration. The name is assumed to be a full name
        (group::namespace:name) if a group name is specified. Otherwise, it's
        taken as the long name of a model.

        :returns: the requested scene component.
        :raises:  an :class:`.ExecutionError` if the component could not be
                  found.
        """
        # Attempt to find the component in the scene by name
        if '::' in self.componentName:
            component = pyfbsdk.FBFindObjectByFullName(self.componentName)
        else:
            component = pyfbsdk.FBFindModelByLabelName(self.componentName)

        # Raise a runtime error if no component exists by the given name
        if not component:
            raise ExecutionError(
                'Could not find a component named "%s" in the scene.' %
                self.componentName)

        # Return the component if found
        return component

    def _setTransformation(self, boxComponent):
        """
        Helper function used by subclasses to set the FBBox to the appropriate
        transformation mode once it's been created, provided it's an instance
        of FBModelPlaceHolder and transformation nodes are to be connected.
        """
        try:
            # Attempt to set the appropriate transformation space if the box
            # declaration's transformation type has been changed from kNone
            if self.transformation == self.TransformationType.kGlobal:
                boxComponent.UseGlobalTransforms = True
            elif self.transformation == self.TransformationType.kLocal:
                boxComponent.UseGlobalTransforms = False
        except AttributeError:
            # If the UseGlobalTransforms attribute isn't present, we're not
            # dealing with an instance of FBModelPlaceHolder after all, so we
            # can simply forget about trying to set the transformation space.
            pass

class SenderBoxDeclaration(PlaceholderBoxDeclaration):
    """
    Defines a type of placeholder box which stands in for a scene object as a
    sender, with its output nodes piping data into the relation constraint.
    """

    def execute(self, constraint, relationComponents):
        """
        Executes the declaration by finding the associated component in the
        scene and adding it to the provided constraint as a sender.

        :returns: the newly created sender box.
        :raises:  an :class:`.ExecutionError` if the named component does not
                  exist or could not be added to the constraint.
        """
        # Find the component to use as a source and create a sender box from it
        component = self._findComponent()
        box = constraint.SetAsSource(component)
        if not box:
            raise ExecutionError(
                'Could not create a sender box for the component "%s".' %
                component.LongName)

        # Set the transformation to global or local as necessary and return the
        # newly created box
        self._setTransformation(box)
        return box

class ReceiverBoxDeclaration(PlaceholderBoxDeclaration):
    """
    Defines a type of placeholder box which constrains a scene object as a
    receiver, with its input nodes receiving data from the relation constraint.
    """

    def execute(self, constraint, relationComponents):
        """
        Executes the declaration by finding the associated component in the
        scene and constraining it in the provided constraint as a receiver.

        :returns: the newly created receiver box.
        :raises:  an :class:`.ExecutionError` if the named component does not
                  exist or could not be added to the constraint.
        """
        # Find the component to constrain and create a receiver box for it
        component = self._findComponent()
        box = constraint.ConstrainObject(component)
        if not box:
            raise ExecutionError(
                'Could not create a receiver box for the component "%s".' %
                component.LongName)

        # Set the transformation to global or local as necessary and return the
        # newly created box
        self._setTransformation(box)
        return box
