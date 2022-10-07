import React from "react"
import { Stack, Typography, Paper, Box, Grid } from "@mui/material";

export default function Filter() {

    return(
        <Paper sx={{border:"1px solid black", p:2.5, backgroundColor: "#e5e5e5", display:"flex"}}>
            <Typography variant="h5" sx={{color: "#1f226a", fontWeight: "bold"}}>
                Filter
            </Typography>
        </Paper>
    )
}