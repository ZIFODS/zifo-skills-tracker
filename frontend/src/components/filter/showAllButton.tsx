import React from "react"
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectHiddenGroups, filterGraphDataRequest, clearHiddenGroups, isGraphDisplayable } from "../graph/graphSlice";
import { selectRuleList } from "../search/searchSlice";

export default function ShowAllButton() {

   const graphDisplayable = useAppSelector(isGraphDisplayable) 

  const dispatch = useAppDispatch()

  let skills = useAppSelector(selectRuleList)
  skills = skills.map(function(skill: any) {return skill.name})

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