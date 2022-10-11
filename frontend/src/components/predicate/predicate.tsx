import React from "react"
import { Stack, Typography, Paper, Box, Grid } from "@mui/material";
import NodeAutocomplete from "./nodeAutocomplete";
import AddRuleButton from "./addRuleButton";
import PredicateList from "./predicateList";
import SearchButton from "./applyButton";
import ClearButton from "./clearButton";

export default function Predicate() {

    return(
        <Paper sx={{border:"1px solid black", p:2.5, backgroundColor: "#e5e5e5", display:"flex", flexGrow: 1}}>
            <Stack justifyContent="space-between">
                <Stack spacing={4}>
                    <Box sx={{borderBottom:"1px solid black", pb: 1}}>
                        <Typography variant="h5" sx={{color: "#1f226a", fontWeight: "bold"}}>
                            Predicates
                        </Typography>
                    </Box>
                    <Stack direction="row" spacing={3} alignItems="flex-end">
                        <NodeAutocomplete />
                        <AddRuleButton/>
                    </Stack>
                    <PredicateList/>
                </Stack>
                <Stack>
                    <ClearButton/>
                    <SearchButton/>
                </Stack>
            </Stack>
        </Paper>
    )
}