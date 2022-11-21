import React from "react";
import { IconButton } from "@mui/material";
import PersonSearchIcon from '@mui/icons-material/PersonSearch';
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectCurrentSearchedConsultant } from "./consultantSlice";
import { getFilterGraphDataByConsultantRequest } from "../graph/graphSlice";

/**
 * Button to apply current consultant search
 */
export default function ConsultantApplyButton() {

  const dispatch = useAppDispatch()

  const searchedConsultant = useAppSelector(selectCurrentSearchedConsultant)

  // Clicking apply button
  const handleClick = () => {
    dispatch(getFilterGraphDataByConsultantRequest({
      query: {
        name: searchedConsultant
      },
      isSearch: true
    }));
  };

  return (
    <IconButton onClick={handleClick}>
      <PersonSearchIcon />
    </IconButton>
  );
}
