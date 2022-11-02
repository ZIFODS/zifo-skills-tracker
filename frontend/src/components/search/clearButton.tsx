import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { clearRuleList, selectRuleList } from "./searchSlice";
import { clearCurrentGraph, getGraphDataRequest } from "../graph/graphSlice";

export default function ClearButton() {
  const dispatch = useAppDispatch();

  const searchList = useAppSelector(selectRuleList);

  const handleClearChange = () => {
    dispatch(clearRuleList());
    dispatch(clearCurrentGraph());
    dispatch(getGraphDataRequest());
  };

  return (
    <Button
      variant="outlined"
      sx={{
        mb: 1,
        p: 0.5,
        fontSize: 15,
        fontWeight: "bold",
        color: "red",
        backgroundColor: "white",
        border: "2px solid red",
      }}
      onClick={handleClearChange}
      disabled={searchList.length === 0}
    >
      Clear
    </Button>
  );
}
