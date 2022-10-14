import React from "react"
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectHiddenGroups, filterGraphDataRequest, isGraphDisplayable, setHiddenGroups, selectCurrentNodes, selectAllNodes } from "../graph/graphSlice";
import { selectRuleList } from "../search/searchSlice";
import { getUniqueGroups } from "../../hooks/useD3";

export default function HideAllButton() {

   const graphDisplayable = useAppSelector(isGraphDisplayable) 

  const dispatch = useAppDispatch()

  const allNodeData = useAppSelector(selectAllNodes)
  const allGroups = getUniqueGroups(allNodeData)

  let skills = useAppSelector(selectRuleList)
  skills = skills.map(function(skill: any) {return skill.name})

  const handleClick = () => {
    const allSkillGroups = allGroups.filter(function(group: string) {return group !== "Consultant"})
    allSkillGroups.map(function(group: string) {dispatch(setHiddenGroups(group))})
    skills.length && dispatch(filterGraphDataRequest({skills: skills, hiddenGroups: allSkillGroups}))
    }

  return(
    <Button variant="outlined" disabled={!graphDisplayable} sx={{p:0.5, fontSize: 10}} onClick={handleClick}>
        Hide all
    </Button>
  )
}