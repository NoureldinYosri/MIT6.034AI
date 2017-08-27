from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem



def get_other(constraint,var):
    name1 = constraint.get_variable_i_name();
    name2 = constraint.get_variable_j_name();
    if name1 == var.get_name():
        return 0,name2;
    else:
        return 1,name1;

def forward_one_var(state,var,assigned = None):
    val = var.get_assigned_value();
    if assigned != None: assert val == assigned;
    tmp = state.get_variable_by_name(var.get_name());
    assert tmp.is_assigned();
    assert tmp.get_assigned_value() == val;
    single = [];
    for constraint in state.get_constraints_by_name(var.get_name()):
        name = constraint.get_variable_j_name();
        var2 = state.get_variable_by_name(name);
        if var2.is_assigned(): continue;
        to_remove = [];
        for val2 in var2.get_domain():
            if not constraint.check(state, val, val2):
                to_remove.append(val2);
        for val2 in to_remove:
            var2.reduce_domain(val2);
        if var2.domain_size() == 0:
            return False,None;
        if var2.domain_size() == 1 and len(to_remove):
            single.append(var2);
    return True,single;


# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    for var in state.get_all_variables():
        if var.is_assigned():
            verdict,_ = forward_one_var(state,var);
            if not verdict: return False;
    return True;
# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False
    # Add your propagate singleton logic here.
    q = [];
    for var in state.get_all_variables():
        if not var.is_assigned() and var.domain_size() == 1:
            q.append(var);
    while len(q):
        var = q.pop(0);
        val = var.get_domain()[0];
        var.set_value(val);
        verdict,aux = forward_one_var(state,var,val);
        if not verdict: return False;
        q.extend(aux);
    return True;

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    from math import sqrt;
    return sqrt(sum(map(lambda x,y: (x - y)**2,list1,list2)));

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 1)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    from math import log
    lg = lambda x: log(x)/log(2);
    val1 = val2 = 0;

    S = set(yes);
    for s in S:
        nc = yes.count(s);
        nb = len(yes) + 0.0;
        val1 += -(nc/nb)*lg(nc/nb);
    S = set(no);
    for s in S:
        nc = no.count(s);
        nb = len(no) + 0.0;
        val2 += -(nc / nb) * lg(nc / nb);
    return (len(yes)*val1 + len(no)*val2)/(len(yes) + len(no));

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 50
rep_classified = limited_house_classifier(house_people, house_votes, N_1)
print rep_classified;
## Find a value of n that classifies at least 90 senators correctly.
N_2 = 100
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
print senator_classified;

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 50
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
print old_senator_classified;

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK =2
WHAT_I_FOUND_INTERESTING = None;
WHAT_I_FOUND_BORING = None;


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
