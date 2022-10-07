import React from "react"
import { Stack, Typography, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectPredicateList } from "./predicateSlice";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import * as d3 from "d3"

export default function PredicateList() {
    const groupDisplayNameLinks: Record<string, string> = {
        Consultant: "Consultant",
        ScienceApps: "Science apps",
        Services: "Services",
        Methodologies: "Methodologies",
        Process: "Processes",
        Other_Products: "Other products",
        Regulatory: "Regulatory",
        Data_Management: "Data management",
        Languages: "Languages",
        programming: "Programming",
        Miscellaneous: "Miscellaneous",
        Infrastructure: "Infrastructure",
    }

    const predicateList = useAppSelector(selectPredicateList)
    const nodeData = useAppSelector(selectAllNodes)
    const groups = getUniqueGroups(nodeData)

    return(
        <Stack spacing={2}>
            {predicateList.map(function(pred: any) {
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