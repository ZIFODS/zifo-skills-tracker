import React from "react"
import { Button } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { filterGraphDataRequest, selectCurrentSearchedNodes, selectHiddenGroups } from "../graph/graphSlice"
import { selectRuleList } from "./searchSlice"

export default function ApplyButton() {

  const dispatch = useAppDispatch()

  const hiddenGroups = useAppSelector(selectHiddenGroups)
  const searchList = useAppSelector(selectRuleList)
  const searchedNodes = useAppSelector(selectCurrentSearchedNodes)
  
  const searchListSkills = searchList.map(function(skill: any) {return skill.name})
  searchListSkills.sort()
  searchedNodes.slice().sort()

  const handleChange = () => {
    searchListSkills.length && dispatch(filterGraphDataRequest({skills: searchListSkills, hiddenGroups: hiddenGroups}))
  }

  const isDisabled = (JSON.stringify(searchListSkills) === JSON.stringify(searchedNodes) || searchListSkills.length === 0)

  return(
    <Button 
      variant="outlined" 
      disabled={isDisabled}
      sx={{ mb: 1, p: 1, fontSize: 15, fontWeight: "bold", color: "white", backgroundColor: !isDisabled ? "#1f226a" : "white", border: "2px solid #1a6714" }}
      onClick={handleChange}
      >
      Apply
    </Button>
  )
}