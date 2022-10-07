import React from "react"
import { Button } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { clearPredicateList, selectPredicateList } from "./predicateSlice"

export default function ClearButton() {

  const dispatch = useAppDispatch()

  const predicateList = useAppSelector(selectPredicateList)

  const handleChange = () => {
    dispatch(clearPredicateList())
  }

  return(
    <Button 
      variant="outlined" 
      sx={{ mb: 1, p: 0.5, fontSize: 15, fontWeight: "bold", color: "red", backgroundColor: "white", border: "2px solid red" }}
      onClick={handleChange}
      disabled={predicateList.length === 0}
      >
      Clear
    </Button>
  )
}