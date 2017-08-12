from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.




def backchain_to_goal_tree(rules, hypothesis):
    ret = OR();
    ret.append(hypothesis);
    for rule in rules:
        A = rule.antecedent();
        B = rule.consequent()[0];
        #print B,hypothesis
        r = match(B,hypothesis);
        #print B,"\t",hypothesis,"\t",r
        if r is None: continue;
        X = populate(A,r);
        if isinstance(X,AND):
            T = AND();
            T.extend([backchain_to_goal_tree(rules,x) for x in X]);
            T = simplify(T);
            ret.append(T);
        elif isinstance(X,OR):
            T = OR();
            T.extend([backchain_to_goal_tree(rules,x) for x in X]);
            T = simplify(T);
            ret.append(T);
        else:
            ret.append(backchain_to_goal_tree(rules,X));
    return simplify(ret);

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')


if __name__ == "__main__":
    RULES = [ IF( AND( '(?x) has (?y)',
                        '(?x) has (?z)' ),
                   THEN( '(?x) has (?y) and (?z)' ) ),
               IF( '(?x) has rhythm and music',
                   THEN( '(?x) could not ask for anything more' ) ) ];
    hyp = 'gershwin could not ask for anything more'
#    print backchain_to_goal_tree(ZOOKEEPER_RULES,'alice is an albatross');
    print backchain_to_goal_tree(RULES,hyp)
