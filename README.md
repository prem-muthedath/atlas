atlas
===========

BOM (bill of materials) costing app.

This OO application, written in Python, computes the cost of each part in a typical BOM (Bill of Materials -- a recursive tree structure of parts and BOMs) and returns the following two results:

1. Total cost of the BOM, which is nothing but the sum of the costs of parts in the BOM.
2. Text and XML representations of parts in the BOM tree and their computed costs.

The problem is complicated because the cost of a part depends on its location in the BOM: its predecessors and successors determine if the part can be costed. This is the business logic side.

The other problem is to collect and present the results (i.e., computed part costs, levels, and other part details) in multiple formats by traversing the BOM's tree structure.  This is the display side.

The display is complex because it allows users to dynamically select and order the fields.


Finally, how to build the BOM tree? By that I mean the sequential addition of parts and sub-BOMs.  The algorithm is a bit tricky, and designing a clean object to do this was a challenge.


HOW TO RUN THE TESTS FROM A TERMINAL:

1. `aenum` package for `python 2.7.16` required; install using `pip` if needed.
2. `cd` to `atlas` directory -- the top directory containing this `README` file.
3. Type the following command:

                python -m atlas

4. Press `ENTER`.
5. You should see THREE things in the output:
   - (a) total cost of the BOM (for 1 run as well as for 2 consecutive runs);
   - (b) indented text representation of parts in BOM & their computed costs;
   - (c) an XML representation of parts in the BOM tree & their computed costs.

  For (b) & (c), you'll get `default` representation as well as a `custom` one.


