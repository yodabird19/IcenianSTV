# IcenianSTV
Python script for implementing STV in accordance with the Constitution of Icenia.

## The relevant Section of the constitution is reproduced below:
When single transferable vote is used in an election with k winners– 
  1. any person entitled to do so may cast a ballot consisting of an ordered ranking of all or a subset of the available choices, beginning at 1;
  2. if k choices have been declared elected, the counting of votes ceases, and the elected choices are the winners;
  3. if there is any choice with more than (total votes)/(k+1) (rounded up to the nearest integer) top-ranked votes (taking weighting into account, and breaking ties in accordance with (5)), where “total votes” corresponds to the total count of non-exhausted voting power–    
     a. the choice with the most top-ranked votes is declared elected;    
     b. all ballots counted towards that choice have their top-ranked vote eliminated, and their voting power is distributed to their next-highest-ranked non-eliminated choice, weighted at (votes received - (total votes/(k+1))/(votes received), where “votes received” represents the number of top-ranked votes received by the elected choice; and    
     c. the protocol repeats starting from (2);
  4. the choice with the fewest top-ranked votes (taking weighting into account, and breaking ties in accordance with (5)) is eliminated, upon which–    
     a. all ballots counted towards that choice have their top-ranked vote eliminated, and their voting power is distributed to their next-highest-ranked non-eliminated choice, weighted fully; and    
     b. the protocol repeats starting from (2);
  5. if two or more choices have an equal number of top-ranked votes (taking weighting into account), ties must be decided by counting second-to-top-ranked votes (taking weighting into account), with the choice with a higher count leading; if this also results in a tie, third-to-top-ranked votes must be counted, and so on; and
  6. if any ballot has all of its votes eliminated, that ballot is declared “exhausted”, its remaining voting power is discounted, and that voting power is subtracted from the count of total votes.
