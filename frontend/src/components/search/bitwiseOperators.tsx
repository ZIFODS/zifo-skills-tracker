import React from "react"
import { Button, Stack, ToggleButtonGroup, ToggleButton } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { clearSearchList, selectSearchList } from "./searchSlice"
import { getGraphDataRequest } from "../graph/graphSlice"
import { useEffect } from "react"

export default function BitwiseOperators() {

  const dispatch = useAppDispatch()

  const searchList = useAppSelector(selectSearchList)

  const [operator, setOperator] = React.useState<string | null>("")

  useEffect(() => {
    if (searchList.length > 0 && operator === "") {
      setOperator("AND")
    }
  }, [searchList])

  const handleOperatorChange = (
    _event: React.MouseEvent<HTMLElement>,
    newOperator: string | null,
  )  => {
    setOperator(newOperator);
  }

  const [parentheses, setParentheses] = React.useState<string | null>("")

  const handleParenthesesChange = (
    _event: React.MouseEvent<HTMLElement>,
    newParentheses: string | null,
  )  => {
    setParentheses(newParentheses);
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
        value={parentheses}
        onChange={handleParenthesesChange}
        exclusive
      >
        <ToggleButton value="[">
          [
        </ToggleButton>
        <ToggleButton value="]">
          ]
        </ToggleButton>
      </ToggleButtonGroup>
    </Stack>
  )
}