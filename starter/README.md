# CS 170 Project Spring 2021

Take a look at the project spec before you get started!

Requirements:

Python 3.6+

You'll only need to install networkx to work with the starter code. For installation instructions, follow: https://networkx.github.io/documentation/stable/install.html

If using pip to download, run `python3 -m pip install networkx`


Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: where you should be writing your code to solve inputs
- `utils.py`: contains functions to compute cost and validate NetworkX graphs

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
  - These are the functions run by the autograder to validate submissions


To run the code:
- `cd` into the starter directory
- To run folders, uncomment the INDIVIDUAL TESTER in `solver.py`
	- Depending on which size of inputs you want to run, replace the `temp` on the `inputs` variable line with `small`, `medium` or `large`
	- Run `python3 solver.py` in the terminal
- To run individual files, uncomment the FOLDER TESTER in `solver.py`
	- Run `python3 solver.py inputs/inputs/{desidered size of graph}/{graph name}` in the terminal (ex: `python3 solver.py inputs/inputs/small/small-126.in` to run the small-126 graph)
- To run on the first solver, change the call to `solve2(H)` in `solver.py` to `solve(H)`.
- To run on different "breaking points"/limit to how many shortest paths to generate for solver2, in `solver.py`, `solver2` function, uncomment/comment/change the `limit` variable.