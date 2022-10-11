import React from "react"
import { Stack, Typography, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectSearchList } from "./searchSlice";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import * as d3 from "d3"
import { groupDisplayNameLinks } from "../../constants/data";

export default function SearchList() {

    const searchList = useAppSelector(selectSearchList)
    const nodeData = useAppSelector(selectAllNodes)
    const groups = getUniqueGroups(nodeData)

    return(
        <Stack spacing={2}>
            {searchList.map(function(pred: any) {
                return(
                    <Paper>
                      <Stack direction="row" alignItems="center">
                          <Typography sx={{backgroundColor: d3.schemePaired[groups.indexOf(pred.group)] + "90", px:1.5, py:1, fontSize: 14}}>{groupDisplayNameLinks[pred.group]}</Typography>
                          <Typography sx={{pl:2, fontSize: 14}}>{pred.name}</Typography>
                      </Stack>
                    </Paper>
                )
            })}
        </Stack>
    )
}