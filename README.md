bom_costing
===========

BOM (Bill of Materials) Costing App

This OO application, written in Python, computes the cost of each part in a typical BOM (Bill of Materials, having a tree structure) and returns the following two results:

1. Total cost of the BOM, which is nothing but the sum of the costs of parts in the BOM.
2. An indented representation of parts in the BOM tree and their computed costs.

The problem is complicated because the cost of a part depends on its location in the BOM: its predecessors and successors determine if the part can be costed. This is the business logic side.

The other complexity is to collect the results (i.e., the computed part costs, levels, and other part details) by traversing the BOM's tree structure.  This data will typically be used for display.

Finally, how to build the BOM tree? By that I mean the sequential addition of parts and sub-BOMs.  The algorithm is a bit tricky, and designing a clean object to do this was a challenge.


I designed small objects to model all this complexity, and it came out pretty neat, after many iterations.  

Because of the problem structure, Composite and Collecting Parameter patterns came in handy (actually, instead of jumping to the patterns, I refactored to them).  

I used Python because it was a good way to learn the language.  Plus, Python was fun.  I loved it!!



HOW TO RUN THE TESTS:

1. Go to bom_costing directory -- THE TOP DIRECTORY OF THE APP, AND IT CONTAINS THIS README FILE.
2. Type the following command: 

		python -m bom_costing.tests.bom_cost_test

3. Press enter.
4. You should see TWO things in the output:
	(a) An indented representation of parts in the BOM tree and their computed costs; 
	(b) Total cost of the BOM -- actual and expected values.
