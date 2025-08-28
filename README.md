# LL(1) Grammar Project

### This project demonstrates how to construct an LL(1) parsing table for a given grammar.  
#### It is organized into three main steps:

1. **Grammar Editing (`grammarEdit.py`)**  
   Removes direct left recursion and performs simple left factoring wherever possible to prepare the grammar for LL(1) parsing.

2. **FIRST and FOLLOW Sets (`first_follow.py`)**  
   Computes the FIRST and FOLLOW sets for all nonterminals in the edited grammar.

3. **LL(1) Parsing Table (`ll1Com.py`)**  
   Builds the LL(1) parsing table if the grammar is LL(1); otherwise, reports conflicts indicating that the grammar is not LL(1).

The entire workflow is managed by `main.py`, which executes these steps in sequence and prints the results.

