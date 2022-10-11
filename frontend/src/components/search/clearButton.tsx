import React from "react"
import { Button } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { clearSearchList, selectSearchList } from "./searchSlice"
import { getGraphDataRequest } from "../graph/graphSlice"
import { useEffect } from "react"

export default function ClearButton() {

  const dispatch = useAppDispatch()

  const searchList = useAppSelector(selectSearchList)

  const handleClearChange = () => {
    dispatch(clearSearchList());
    dispatch(getGraphDataRequest());
  }

  return(
    <Button 
      variant="outlined" 
      sx={{ mb: 1, p: 0.5, fontSize: 15, fontWeight: "bold", color: "red", backgroundColor: "white", border: "2px solid red" }}
      onClick={handleClearChange}
      disabled={searchList.length === 0}
      >
      Clear
    </Button>
  )
}