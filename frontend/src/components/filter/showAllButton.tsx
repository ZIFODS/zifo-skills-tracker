import React from "react"
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { filterGraphDataRequest, clearHiddenGroups, isGraphDisplayable, selectCurrentSearchedNodes } from "../graph/graphSlice";

export default function ShowAllButton() {

   const graphDisplayable = useAppSelector(isGraphDisplayable) 

  const dispatch = useAppDispatch()

  let skills = useAppSelector(selectCurrentSearchedNodes)

  const handleClick = () => {
    dispatch(clearHiddenGroups())
    skills.length && dispatch(filterGraphDataRequest({skills: skills, hiddenGroups: []}))
    }

  return(
    <Button variant="outlined" disabled={!graphDisplayable} sx={{p:0.5, fontSize: 10}} onClick={handleClick}>
        Show all
    </Button>
  )
}