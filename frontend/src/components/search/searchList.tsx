import React from "react";
import { Stack, Paper, Box } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectSearchList } from "./searchSlice";
import SearchSkill from "./searchSkill";
import SearchOperator from "./searchOperator";
import { useEffect } from "react";

/**
 * Component displaying list of skills to be searched
 */
export default function SearchList() {
  const searchList = useAppSelector(selectSearchList);

  /**
   * Get indices in search list where parenthesis matches supplied character.
   *
   * @param {string} char [ or ] character
   * @return {number[]} Indices of matching skills in search list
   */
  const getBracketIndexes = (char: string) => {
    return searchList
      .map((item: any, index: number) => ({ ...item, index }))
      .filter((item: any) => item.parenthesis == char)
      .map((item: any) => item.index);
  };

  // Get indices of open and closed parentheses
  let startBracketIdxs = getBracketIndexes("[");
  let endBracketIdxs = getBracketIndexes("]");

  // Update parenthesis indices when search list changes
  useEffect(() => {
    startBracketIdxs = getBracketIndexes("[");
    endBracketIdxs = getBracketIndexes("]");
  }, [searchList]);

  let open = false;

  return (
    <Stack sx={{flex: 1}} spacing={1}>
      {searchList.map(function (rule: any, j: number) {
        // Determine if bracket is open
        if (rule.parenthesis === "[") {
          open = true;
        }
        if (rule.parenthesis === "]") {
          open = false;
        }

        // If bracket is closed return node normally
        if (!open && !endBracketIdxs.includes(j)) {
          return (
            <Stack spacing={1}>
              {rule.operator !== "" &&
                (endBracketIdxs.map((idx: number) => idx + 1).includes(j) ||
                  j !== 0) && <SearchOperator operator={rule.operator} />}
              <SearchSkill group={rule.group} name={rule.name} />
            </Stack>
          );
        }

        // If bracket is open then it should be wrapped in yellow paper
        // Nothing should be returned until either last node or closed parenthesis
        else if (endBracketIdxs.includes(j) || j === searchList.length - 1) {
          let startBracketIdx = startBracketIdxs[endBracketIdxs.indexOf(j)];
          if (startBracketIdx === undefined) {
            startBracketIdx = startBracketIdxs.slice(-1)[0];
          }
          const nodesInParentheses = searchList.filter(function (
            rule: any,
            k: number
          ) {
            return k >= startBracketIdx && k <= j;
          });
          return (
            <Stack spacing={1}>
              <SearchOperator operator={searchList[startBracketIdx].operator} />
              <Paper sx={{ p: 1, py: 1.5, backgroundColor: "#e6d4aa" }}>
                <Stack spacing={1}>
                  {nodesInParentheses.map(function (rule: any, k: number) {
                    return (
                      <Stack spacing={1}>
                        {rule.operator !== "" && k !== 0 && (
                          <SearchOperator operator={rule.operator} />
                        )}
                        <SearchSkill group={rule.group} name={rule.name} />
                      </Stack>
                    );
                  })}
                </Stack>
              </Paper>
            </Stack>
          );
        }
      })}
    </Stack>
  );
}
