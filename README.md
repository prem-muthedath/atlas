bom_costing
===========

BOM (Bill of Materials) Costing App

This OO application, written in Python, computes the cost of each part in a typical BOM (Bill of Materials -- a recursive tree structure of parts and BOMs) and returns the following two results:

1. Total cost of the BOM, which is nothing but the sum of the costs of parts in the BOM.
2. Text and XML representations of parts in the BOM tree and their computed costs.

The problem is complicated because the cost of a part depends on its location in the BOM: its predecessors and successors determine if the part can be costed. This is the business logic side.

The other problem is to collect and present the results (i.e., computed part costs, levels, and other part details) in multiple formats by traversing the BOM's tree structure.  This is the display side.

The display is complex because it allows users to dynamically select and order the fields.

For default & custom diplay creations, see default.py & custom.py in bom_costing/bom_costing/tests.


Finally, how to build the BOM tree? By that I mean the sequential addition of parts and sub-BOMs.  The algorithm is a bit tricky, and designing a clean object to do this was a challenge.


I designed small objects to model all this complexity, and it came out pretty neat, after many iterations.

Because of the problem structure, Composite, Collecting Parameter, and Visitor patterns came in handy (actually, instead of jumping to the patterns, I refactored to them).

I used Python because it was a good way to learn the language.  Plus, Python was fun.  I loved it!!



HOW TO RUN THE TESTS FROM A TERMINAL:

1. cd to bom_costing directory -- the top directory of the app containing this README file.
2. Type the following command:

		python -m bom_costing

3. Press enter.
4. You should see THREE things in the output:
	(a) Total cost of the BOM -- actual and expected values;
	(b) An indented Textual representation of parts in the BOM tree and their computed costs;
	(c) An XML representation of parts in the BOM tree and their computed costs.

  For items (b) and (c), you should see a default representation as well as a customised one.


