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

  return(
    <Stack spacing={1}>
      {searchList.map(function(pred: any) {
        console.log(pred.value)
        return(
          pred.type === "node" ? 
          <Paper>
            <Stack direction="row" alignItems="center">
              <Typography sx={{backgroundColor: d3.schemePaired[groups.indexOf(pred.value.group)] + "90", px:1.5, py:1, fontSize: 14}}>{groupDisplayNameLinks[pred.value.group]}</Typography>
              <Typography sx={{pl:2, fontSize: 14}}>{pred.value.name}</Typography>
            </Stack>
          </Paper>
          : pred.value.operator !== "" &&
          <Typography variant="subtitle2" sx={{px: 1, fontWeight:"bold"}}>
            {pred.value.operator}
          </Typography>
          )
      })}
    </Stack>
  )
}