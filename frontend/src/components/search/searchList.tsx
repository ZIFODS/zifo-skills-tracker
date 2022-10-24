import React from "react"
import { Stack, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectRuleList } from "./searchSlice";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import RuleSkill from "./ruleSkill";
import RuleOperator from "./ruleOperator";
import { useEffect } from "react";


export default function SearchList() {

  const searchList = useAppSelector(selectRuleList)
  const nodeData = useAppSelector(selectAllNodes)

  let open = false

  const getBracketIndexes = (char: string) => {
    return searchList
      .map((item: any, index: number) => ({...item, index}))
      .filter((item: any) => item.parenthesis == char)
      .map((item: any) => item.index)
  }

  let startBracketIdxs = getBracketIndexes("[")
  let endBracketIdxs = getBracketIndexes("]")

  useEffect(() => {
    startBracketIdxs = getBracketIndexes("[")
    endBracketIdxs = getBracketIndexes("]")
  }, [searchList])

  return(
    <Stack spacing={1}>
      {searchList.map(function(rule: any, j: number) {

      // determine if bracket is open
      if (rule.parenthesis === "[") {
        open = true
      }
      if (rule.parenthesis === "]") {
        open = false
      }

      // if bracket is closed return node normally
      if (!open && !endBracketIdxs.includes(j)) {
        return(
          <Stack spacing={1}>
            {(rule.operator !== "" && (endBracketIdxs.map((idx: number) => idx + 1).includes(j) || j !==0)) &&
              <RuleOperator operator={rule.operator}/>
            }
            <RuleSkill group={rule.group} name={rule.name} />
          </Stack>
          )
      }

      // if bracket is open then it should be wrapped in yellow paper - nothing should be returned until bracket closed
      else if (endBracketIdxs.includes(j) || j === searchList.length - 1) {
        let startBracketIdx = startBracketIdxs[endBracketIdxs.indexOf(j)]
        if (startBracketIdx === undefined) {
          startBracketIdx = startBracketIdxs.slice(-1)[0]
        }
        const nodesInParentheses = searchList.filter(function(rule: any, k: number) {
          return (k >= startBracketIdx && k <= j)
        })
        return(
          <Stack spacing={1}>
            <RuleOperator operator={searchList[startBracketIdx].operator}/>
              <Paper sx={{p: 1, py:1.5, backgroundColor: "#e6d4aa"}}>
                <Stack spacing={1}>
                {nodesInParentheses.map(function(rule: any, k: number) {
                    return (
                      <Stack spacing={1}>
                        {(rule.operator !== "" && k !== 0) &&
                        <RuleOperator operator={rule.operator}/>
                        }
                        <RuleSkill group={rule.group} name={rule.name} />
                      </Stack>
                    )
                  }
                )}
                </Stack>
              </Paper>
            </Stack>
          )
        }
      })}
    </Stack>
  )
}