import React from "react"
import { IconButton } from "@mui/material"
import AddIcon from '@mui/icons-material/Add';
import { useAppDispatch } from "../../app/hooks";
import { addCurrentPredicateToList } from "./predicateSlice";

export default function AddRuleButton() {
    const dispatch = useAppDispatch()

    const handleClick = () => {
        dispatch(addCurrentPredicateToList())
    }

    return(
        <IconButton onClick={handleClick}>
            <AddIcon/>
        </IconButton>
    )
}