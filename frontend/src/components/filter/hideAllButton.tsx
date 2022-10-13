import React from "react"
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectHiddenGroups, filterGraphDataRequest, isGraphDisplayable, setHiddenGroups, selectCurrentNodes } from "../graph/graphSlice";
import { selectRuleList } from "../search/searchSlice";
import { getUniqueGroups } from "../../hooks/useD3";

export default function HideAllButton() {

   const graphDisplayable = useAppSelector(isGraphDisplayable) 

  const dispatch = useAppDispatch()

  const currentNodeData = useAppSelector(selectCurrentNodes)
  const currentGroups = getUniqueGroups(currentNodeData)
  const hiddenGroups = useAppSelector(selectHiddenGroups)

  let skills = useAppSelector(selectRuleList)
  skills = skills.map(function(skill: any) {return skill.name})

  const handleClick = () => {
    currentGroups.map(function(group: string) {dispatch(setHiddenGroups(group))})
    skills.length && dispatch(filterGraphDataRequest({skills: skills, hiddenGroups: currentGroups}))
    }

  return(
    <Button variant="outlined" disabled={!graphDisplayable} sx={{p:0.5, fontSize: 10}} onClick={handleClick}>
        Hide all
    </Button>
  )
}