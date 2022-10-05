James Corby 

Overview: 

This folder contains the building of a model that is used to determine the exposure rating for a selection of UAVs.
Only the information provided and generic python coding has been used to perform the required calculations. However in order 
to calculate the ILF using the Riebesell formula, the 'math' module has been imported to make use of the log() fucntion. 

Some things i noticed before starting:
- The JSON dictionary provided is not complete -> Ive had to add the TPL Limit and TPL Excess to fix syntax errors. 
- The serial numbers in the example data do not match the excel spreadsheet. Ive assumed that drone AAA-123 is CCC-333. 

How to execute the code: 
- In the terminal run python model.py

Thoughts:

The model i have built has been implemented for ease of reading. There are many ways this model can be improved in terms
of its speed. For example, to speed up the calculations i could move all code to be indented within a single for loop. However,
ive decided to design the code so that its clear what calculations are being made.

Further, to make the code more scalable to involve more complex calculations i feel that a model class would be more sufficient 
so that certain model calculations can be imbedded into particular methods. For example a method for drone calculations and a method
for cameras etc. 

Final words:

I found the calculation of the ILF formula the hardest as ive never come across the idea of a 'limiting factor' before especially 
using the Riebesell formula. However, after doing some extra days research i came to discover how the formula is structured and managed 
to reproduce the correct calculations.

i really enjoyed this task, i hope it meets the standards. Any questions please ask!