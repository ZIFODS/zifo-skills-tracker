import React from "react"
import { IconButton } from "@mui/material"
import AddIcon from '@mui/icons-material/Add';
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { addCurrentRulesToList, clearCurrentNodeSearch } from "./searchSlice";

export default function AddRuleButton() {

    const dispatch = useAppDispatch()

    const handleClick = () => {
        dispatch(addCurrentRulesToList())
        dispatch(clearCurrentNodeSearch())
    }

    return(
        <IconButton onClick={handleClick}>
            <AddIcon/>
        </IconButton>
    )
}