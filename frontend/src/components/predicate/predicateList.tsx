import React from "react"
import { Stack, Typography, Paper } from "@mui/material";

interface IPredicateList {
    predicates: Array<Record<string, string>>
}

export default function PredicateList({predicates}: IPredicateList) {
    const colorGroupLinks: Record<string, string> = {
        Consultant: "#cbe4f9",
        ScienceApps: "#eff9da",
        Services: "#f9d8d6",
        Methodologies: "#cdf5f6",
        Process: "#d6cdea",
        Other_Products: "#cdf5f6",
        Regulatory: "#f9ebdf",
        Data_Management: "#d6cdea",
        Languages: "#cbe4f9",
        programming: "#eff9da",
        Miscellaneous: "#f9d8d6",
        Infrastructure: "#f9ebdf",
    }
    return(
        <Stack>
            {predicates.map(function(pred: any) {
                return(
                    <Paper>
                      <Stack direction="row" alignItems="center">
                          <Typography sx={{backgroundColor: colorGroupLinks[pred.group], px:1.5, py:1}}>{pred.group}</Typography>
                          <Typography sx={{pl:2}}>{pred.node}</Typography>
                      </Stack>
                    </Paper>
                )
            })}
        </Stack>
    )
}