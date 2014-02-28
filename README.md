ZapposSearch
============

Search for n items given an x total and return lists of combinations

Some Design Decisions:
Given that Zappos has thousands of items, only the subset allowed by the budget is checked. Then to avoid the 
inefficient method of finding solutions, rather than creating possible price combinations of n items and then 
rejecting or accepting them, the algorithm should instead start at an average price and proportionately moving
some values up and some values down. 

Two kinds of buying behaviors are typical. The average set that has a person buying gifts for people who are of
equal importance and likely an equal portion of the budget will be alloted to them and the set where gifts are 
on opposite ends in price, for a more heirarchical setup. So two examples would be buying for your kids or friends
versus buying for a boss and coworkers or spouse and kids. Mainly, the average case is more typical and is more 
represented in the combinations, but the starting condition does have the amounts at opposite poles.

Also, the algorithm does not reject solutions of buying three of the same item at the same price. When buying for 
triplets, or friends, it is sometimes preferential to buy the same item, so those solutions were kept. 

No language was specified for the Challenge. Python was chosen for its ease with networking and the lack of 
code overhead. The biggest differences, had it been written in Java, would be that dictionaries would be hash
tables, the networking would have to be done in its API, and some of the methods would likely be longer due
to the shortcuts of array manipulation allowed in Python. 

The slowest part in testing was the query to the site and on Thursday evening during final testing stages the 
requests were being throttled. I limit how many pages of results return with the local variable to the search function
named limit.

I was able to test the querying code on Wednesday, and it seemed to work, but the
rest of the program was tested on local input.
