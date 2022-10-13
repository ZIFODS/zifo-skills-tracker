import React from "react"
import { Stack, Typography, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectRuleList } from "./searchSlice";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import * as d3 from "d3"
import { groupDisplayNameLinks } from "../../constants/data";

export default function SearchList() {

  const searchList = useAppSelector(selectRuleList)
  const nodeData = useAppSelector(selectAllNodes)
  const groups = getUniqueGroups(nodeData)

  let open = false

  const startBracketIdx = searchList.map(function(rule: any, i:number) {return(rule.parenthesis)}).indexOf("[")
  const endBracketIdx = searchList.map(function(rule: any, i:number) {return(rule.parenthesis)}).indexOf("]")

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
      if (!open && j !== endBracketIdx) {
        return(
          <Stack spacing={1}>
            {(rule.operator !== "" && (j === endBracketIdx + 1 || j !==0)) &&
              <Typography variant="subtitle2" sx={{px: 1, fontWeight:"bold"}}>
                {rule.operator}
              </Typography>
            }
            <Paper>
              <Stack direction="row" alignItems="center">
                <Typography sx={{backgroundColor: d3.schemePaired[groups.indexOf(rule.group)] + "90", px:1.5, py:1, fontSize: 14}}>{groupDisplayNameLinks[rule.group]}</Typography>
                <Typography sx={{pl:2, fontSize: 14}}>{rule.name}</Typography>
              </Stack>
            </Paper>
            {(startBracketIdx !== -1 && j === startBracketIdx - 1) &&
            <Typography variant="subtitle2" sx={{px: 1, fontWeight:"bold"}}>
              {searchList[startBracketIdx].operator}
            </Typography>
            }
          </Stack>
          )
      }

      // if bracket is open then it should be wrapped in yellow paper - nothing should be returned until bracket closed
      else if (j === endBracketIdx || j === searchList.length - 1) {
        const endIdx = endBracketIdx === -1 ? searchList.length - 1 : endBracketIdx
        const nodesInParentheses = searchList.filter(function(rule: any, k: number) {
          return (k >= startBracketIdx && k <= endIdx)
        })
        return(
            <Paper sx={{p: 1, py:1.5, backgroundColor: "#e6d4aa"}}>
              <Stack spacing={1}>
              {nodesInParentheses.map(function(rule: any, k: number) {
                  return (
                    <Stack spacing={1}>
                      {(rule.operator !== "" && k !== 0) &&
                      <Typography variant="subtitle2" sx={{px: 1, fontWeight:"bold"}}>
                        {rule.operator}
                      </Typography>
                      }
                      <Paper>
                        <Stack direction="row" alignItems="center">
                          <Typography sx={{backgroundColor: d3.schemePaired[groups.indexOf(rule.group)] + "90", px:1.5, py:1, fontSize: 14}}>{groupDisplayNameLinks[rule.group]}</Typography>
                          <Typography sx={{pl:2, fontSize: 14}}>{rule.name}</Typography>
                        </Stack>
                      </Paper>
                    </Stack>
                  )
                }
              )}
              </Stack>
            </Paper>
          )
        }
      })}
    </Stack>
  )
}