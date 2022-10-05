import React from "react"
import { Button } from "@mui/material"

export default function SearchButton() {
    return(
        <Button variant="outlined" sx={{mb: 1, p: 2, fontSize: 15, fontWeight: "bold", color: "white", backgroundColor: "#1f226a", border: "2px solid #1a6714"}}>
            Search
        </Button>
    )
}