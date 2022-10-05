import React from "react"
import { Autocomplete, TextField } from "@mui/material";

export default function NodeAutocomplete() {
    const nodes = [
        "test",
        "test2"
    ]
    return(
        <Autocomplete
            disablePortal
            id="combo-box-demo"
            sx={{fontSize: 14}}
            options={nodes}
            renderInput={
                (params) => <TextField {...params} label="Node" variant="standard" sx={{minWidth:200}} InputLabelProps={{style: {fontSize: 14}}}/>}
        />
    )
}