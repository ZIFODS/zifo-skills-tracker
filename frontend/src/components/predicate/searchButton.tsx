import React from "react"
import { Button } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { filterGraphDataRequest } from "../graph/graphSlice"
import { selectPredicateList } from "./predicateSlice"

export default function SearchButton() {

  const dispatch = useAppDispatch()

  let skills = useAppSelector(selectPredicateList)
  skills = skills.map(function(skill: any) {return skill.name})

  const handleChange = () => {
    skills.length && dispatch(filterGraphDataRequest(skills))
  }

  return(
    <Button 
      variant="outlined" 
      sx={{ mb: 1, p: 2, fontSize: 15, fontWeight: "bold", color: "white", backgroundColor: "#1f226a", border: "2px solid #1a6714" }}
      onClick={handleChange}
      >
      Search
    </Button>
  )
}