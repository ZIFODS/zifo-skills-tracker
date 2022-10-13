import React from "react"
import { Stack, ToggleButtonGroup, ToggleButton } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { selectCurrentSearchOperator, selectCurrentSearchParenthesis, selectRuleList, setCurrentBitwiseOperatorSearch } from "./searchSlice"
import { useEffect } from "react"

export default function BitwiseOperators() {

  const dispatch = useAppDispatch()

  const operator = useAppSelector(selectCurrentSearchOperator)
  let parenthesis = useAppSelector(selectCurrentSearchParenthesis)
  const searchList = useAppSelector(selectRuleList)

  const numOpenParentheses = searchList.filter(function(rule: any) {return rule.parenthesis === "["}).length
  const numClosedParentheses = searchList.filter(function(rule: any) {return rule.parenthesis === "]"}).length
  let parenthesesOpen = false
  if (numOpenParentheses > 0) {
    if (numClosedParentheses === 0) {
      parenthesesOpen = true
      if (parenthesis !== "]") {
        parenthesis = ""
      } 
    }
    if (numClosedParentheses > 0) {
      if (parenthesis !== "[") {
        parenthesis = ""
      } 
    }
  }

  useEffect(() => {
    if (searchList.length > 0 && operator === "") {
      dispatch(setCurrentBitwiseOperatorSearch({operator: "AND", parenthesis: parenthesis}))
    }
    else if (searchList.length === 0) {
      dispatch(setCurrentBitwiseOperatorSearch({operator: "", parenthesis: ""}))
    }
  }, [searchList])

  const handleOperatorChange = (
    _event: React.MouseEvent<HTMLElement>,
    newOperator: string | null,
  )  => {
    dispatch(setCurrentBitwiseOperatorSearch({operator: newOperator, parenthesis: parenthesis}));
  }

  const handleParenthesisChange = (
    _event: React.MouseEvent<HTMLElement>,
    newParentheses: string | null,
  )  => {
    dispatch(setCurrentBitwiseOperatorSearch({operator: operator, parenthesis: newParentheses}));
  }

  return(
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
  )
}