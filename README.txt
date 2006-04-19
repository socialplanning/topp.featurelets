Featurelets is a package that provides an infrastructure for, well,
um, "featurelets".  I know, I know, the next question, and rightly so,
is "What is a featurelet?"  Put most simply, featurelets are feature
plug-ins, little bundles of functionality that can be installed into a
particular location within a CMF site.  It's a very simple concept,
but is a bit hard to explain in the abstract, so a concrete example
would probably be helpful.

In the OpenPlans site (http://www.openplans.org/), anyone can create a
project.  In these projects, we offer feature modules that can be
turned on and off.  The optional features that someone might want to
add to her project include, for instance, a project roster, or
blogging capabilities, or mailing lists.  Each of these is a
featurelet.  The project, into which the featurelets are installed is
a "featurelet supporter".

Featurelets are deliberately vague so that they can be flexible.  Each
featurelet contains a "package", and when a featurelet is installed
into a featurelet supporter this package is delivered to the
supporter.  Common operations associated w/ the delivery of a package
include the creation of content objects and the registration of menu
items; support for both of these operations are built into the
featurelets core.  It's possible to make a featurelet do anything,
however, provided the featurelet supporter can support the operations.
To ensure this, featurelets support the idea of required interfaces;
if a featurelet is installed into a supporter that does not implement
or adapt to all of the featurelet's required interfaces, an adaptation
exception will be raised.
