from typing import NamedTuple

from app.models.rule import Rule

class BracketIndexes(NamedTuple):
    start: int
    end: int

def determine_effective_bracket_indexes(rules: list[Rule]) -> list[BracketIndexes]:
    """
    Determine index ranges of effective brackets in search list.
    If bracket not closed, end of search list is classed as closing bracket.
    Returns empty list if no parenthesis present.
    
    Arguments
    ---------
    rules : list[Rule]
        list of rules in search list

    Returns
    -------
    bracket_idx_list : list[BracketIndexes]
        list of start and end indexes for effective brackets
    """
    bracket_idx_list = []
    final_i = len(rules) - 1

    for i, rule in enumerate(rules):
        
        current_parenthesis = rule["parenthesis"]

        # If index at start of bracket, add index pair with start and end equal to index
        if i == 0:
            bracket_idx_list.append(BracketIndexes(i, i))

        elif current_parenthesis == "[":
            bracket_idx_list.append(BracketIndexes(i, i))

        else:
            previous_parenthesis = rules[i-1]["parenthesis"]

            if previous_parenthesis == "]":
                bracket_idx_list.append(BracketIndexes(i, i))

        # If index at end of bracket, extend most recent index pair to current index
        if bracket_idx_list:
            last_bracket_idx = bracket_idx_list[-1]
            if i == final_i:
                bracket_idx_list[-1] = BracketIndexes(last_bracket_idx.start, i)

            elif current_parenthesis == "]":
                bracket_idx_list[-1] = BracketIndexes(last_bracket_idx.start, i)

            else:
                next_parenthesis = rules[i + 1]["parenthesis"]

                if next_parenthesis == "[":
                    bracket_idx_list[-1] = BracketIndexes(last_bracket_idx.start, i)
   
    return bracket_idx_list

class OrStatus(NamedTuple):
    is_or: bool
    start_or: bool
    end_or: bool

class OrStatusProcesser:
    def _not(self):
        return OrStatus(False, False, False)

    def _start(self):
        return OrStatus(True, True, False)

    def _middle(self):
        return OrStatus(True, False, False)

    def _end(self):
        return OrStatus(True, False, True)

    def process(self, i: int, rules: list[Rule]) -> OrStatus:
        """
        Determine if current index is within, first element of, or last element of OR sequence.

        Arguments
        ---------
        i : int
            current index of rule in search list
        rules: list[Rule]
            all rules in search list
        
        Returns
        -------
        or_status : OrStatus
            OR sequence information for current rule
        """
        rule = rules[i]

        final_i = len(rules) - 1

        current_operator = rule["operator"]
        current_parenthesis = rule["parenthesis"]

        if i != final_i:
            next_operator = rules[i + 1]["operator"]
            next_parenthesis = rules[i + 1]["parenthesis"]

            # For first rule, if next operator is OR then it's start of OR sequence, otherwise not.
            if i == 0:
                if next_operator == "OR":
                    return self._start()
                else:
                    return self._not()

            else:
                previous_operator = rules[i - 1]["operator"]
                previous_parenthesis = rules[i - 1]["parenthesis"]

                # If neither the current nor next operators are OR then not part of OR sequence
                if current_operator != "OR" and next_operator != "OR":
                    return self._not()

                # If next operator is OR and it's end of bracket - if previous was OR then end of sequence otherwise not OR
                # Otherwise if it's either start of bracket or first OR then it's start of OR sequence
                # Otherwise if next operator is still OR then it's in middle of OR sequence
                if next_operator == "OR":

                    if current_parenthesis == "]":
                        if previous_operator == "OR":
                            return self._end()

                        return self._not()

                    elif current_operator != "OR" or previous_parenthesis == "]" or current_parenthesis == "[":
                        return self._start() 

                    return self._middle()

                # If current operator is OR and isn't start of bracket then it's within OR sequence but can't be start
                elif current_operator == "OR" and current_parenthesis != "[":
                    # If next operator is not OR or end of bracket then it's end of OR sequence
                    # Otherwise it's in middle of OR sequence
                    if next_operator != "OR" or current_parenthesis == "]" or next_parenthesis == "[":
                        return self._end()

                    return self._middle()

                return self._not()

        else:
            # If one skill in list then can't be part of OR sequence
            if i == 0:
                return self._not()

            # If it's the final skill, current operator is OR and not start of bracket then it's end of OR sequence
            elif current_operator == "OR":
                if current_parenthesis != "[":
                    return self._end()

            # If last operator not OR then not part of OR sequence
            return self._not()

def get_all_end_brackets(bracket_idx_list: list[BracketIndexes]) -> list[int]:
    """
    Get all indexes of end of brackets in bracket index list.

    Arguments
    ---------
    bracket_idx_list: list[BracketIndexes]
        list of start and end indexes for effective brackets

    Returns
    -------
    list[int]
        end bracket indexes
    """
    return [i[1] for i in bracket_idx_list]

def is_index_at_end_of_bracket(i: int, bracket_idx_list: list[BracketIndexes]) -> bool:
    """
    Check if current index of rule is at the end of a bracket.

    Arguments
    ---------
    i : int
        current index of rule
    bracket_idx_list : list[BracketIndexes]
        list of start and end indexes for effective brackets
    
    Returns
    -------
    bool
        if current index at end of bracket
    """
    end_bracket_idxs = get_all_end_brackets(bracket_idx_list)

    # TODO: is check to not be first element actually needed? If so, update docstring
    return (i in end_bracket_idxs and i != end_bracket_idxs[0])

def increment_path_count(path_count: int, or_status: OrStatus, parenthesis: str, is_index_at_end_of_bracket: bool) -> int:
    """
    Increment Cypher path count based on processing of current rule.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    or_status : OrStatus
        or sequence status for current rule
    parenthesis : str
        parenthesis character for current rule
    is_index_at_end_of_bracket : bool
        if apoc intersect or union query has been generated

    Results
    -------
    path_count : int
        incremented number of Cypher paths
    """
    if parenthesis == "]":
        path_count += 1
    elif not or_status.is_or:
        path_count += 1
    elif or_status.end_or:
        path_count += 1

    if is_index_at_end_of_bracket:
        path_count += 2

    return path_count