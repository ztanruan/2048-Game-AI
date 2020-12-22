Hello students,  

Here is the feedback on your proposal.  As with all teams, I am requiring a modification to the normal game rules to ensure that no group can simply copy their project implementation from code that exists online.  

Here is your rule modification: In addition to the standard actions, the agent can also choose to rotate the tiles in the 2x2 square in the middle of the board by +/- 90 degrees.  This action will not produce any merged tiles itself but may enable other good merges in subsequent actions.  Keep in mind that as part of the project guidelines you need to consider multiple problem sizes (for example, different sized boards).  

For tree search, expectimax would be more appropriate than minimax since the "opponent" is random and not adversarial.  

For state representation, what you propose might work and is worth trying.  If it become problematic, you could also try some other things.  One idea is to store the base-2 logarithm of each tile in M instead of its actual value.  Another is to make M a 3D array, for example 4x4x16, where the third dimension is a 0/1 array which stores the tile's value in binary code.  Other ideas might be possible too.  

If you have any questions or concerns about this feedback don't hesitate to reach out.  Best,  


Garrett Katz  