import React from "react"
import { Stack, Typography, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectPredicateList } from "./predicateSlice";

export default function PredicateList() {
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

    return(
        <Stack spacing={2}>
            {predicateList.map(function(pred: any) {
                return(
                    <Paper>
                      <Stack direction="row" alignItems="center">
                          <Typography sx={{backgroundColor: colorGroupLinks[pred.group], px:1.5, py:1, fontSize: 14}}>{groupDisplayNameLinks[pred.group]}</Typography>
                          <Typography sx={{pl:2, fontSize: 14}}>{pred.name}</Typography>
                      </Stack>
                    </Paper>
                )
            })}
        </Stack>
    )
}