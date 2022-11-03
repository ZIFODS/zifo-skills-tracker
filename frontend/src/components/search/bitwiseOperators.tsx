import React from "react";
import { Stack, ToggleButtonGroup, ToggleButton } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  clearCurrentParenthesis,
  selectCurrentSearchOperator,
  selectCurrentSearchParenthesis,
  selectRuleList,
  setCurrentBitwiseOperatorSearch,
} from "./searchSlice";
import { useEffect } from "react";

/**
 * Toggle buttons for bitwise operators and parentheses.
 */
export default function BitwiseOperators() {

  const dispatch = useAppDispatch();

  const operator = useAppSelector(selectCurrentSearchOperator);
  let parenthesis = useAppSelector(selectCurrentSearchParenthesis);
  const searchList = useAppSelector(selectRuleList);

  // Determine if parentheses are open or closed in current search list
  const numOpenParentheses = searchList.filter(function (rule: any) {
    return rule.parenthesis === "[";
  }).length;
  const numClosedParentheses = searchList.filter(function (rule: any) {
    return rule.parenthesis === "]";
  }).length;
  
  let parenthesesOpen = false;
  if (numOpenParentheses === numClosedParentheses) {
    parenthesesOpen = false;
  } else {
    parenthesesOpen = true;
  }
 
  useEffect(() => {
    dispatch(clearCurrentParenthesis());
    // If search list filled and operator not selected, default is AND
    if (searchList.length > 0 && operator === "") {
      dispatch(
        setCurrentBitwiseOperatorSearch({ operator: "AND", parenthesis: "" })
      );
    }
    // If search list empty, no operator or parenthesis
    if (searchList.length === 0) {
      dispatch(
        setCurrentBitwiseOperatorSearch({ operator: "", parenthesis: "" })
      );
    }
  }, [searchList]);

  // Clicking bitwise operator toggle button
  const handleOperatorChange = (
    _event: React.MouseEvent<HTMLElement>,
    newOperator: string | null
  ) => {
    if (newOperator !== null) {
      dispatch(
        setCurrentBitwiseOperatorSearch({
          operator: newOperator,
          parenthesis: parenthesis,
        })
      );
    }
  };

  // Clicking parenthesis toggle button
  const handleParenthesisChange = (
    _event: React.MouseEvent<HTMLElement>,
    newParentheses: string | null
  ) => {
    dispatch(
      setCurrentBitwiseOperatorSearch({
        operator: operator,
        parenthesis: newParentheses,
      })
    );
  };

  return (
    <Stack direction="row" spacing={2}>
      <ToggleButtonGroup
        value={operator}
        exclusive
        onChange={handleOperatorChange}
      >
        <ToggleButton value="AND" disabled={searchList.length === 0}>
          AND
        </ToggleButton>
        <ToggleButton value="OR" disabled={searchList.length === 0}>
          OR
        </ToggleButton>
      </ToggleButtonGroup>
      <ToggleButtonGroup
        value={parenthesis}
        onChange={handleParenthesisChange}
        exclusive
      >
        <ToggleButton value="[" disabled={parenthesesOpen}>
          [
        </ToggleButton>
        <ToggleButton value="]" disabled={!parenthesesOpen}>
          ]
        </ToggleButton>
      </ToggleButtonGroup>
    </Stack>
  );
}
