import React from "react";
import { IconButton } from "@mui/material";
import PersonSearchIcon from '@mui/icons-material/PersonSearch';
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { clearCurrentConsultantToSearch, selectCurrentConsultantToSearch, setCurrentConsultantSearched } from "./consultantSlice";
import { clearHiddenGroups, getFilterGraphDataByConsultantRequest, getSearchGraphDataByConsultantRequest } from "../graph/graphSlice";

/**
 * Button to apply current consultant search
 */
export default function ConsultantApplyButton() {

  const dispatch = useAppDispatch()

  const consultantToSearch = useAppSelector(selectCurrentConsultantToSearch)

  // Clicking apply button
  const handleClick = () => {
    dispatch(getSearchGraphDataByConsultantRequest({
      name: consultantToSearch
    }));
    dispatch(getFilterGraphDataByConsultantRequest({
      name: consultantToSearch,
      hiddenGroups: []
    }));
    dispatch(clearHiddenGroups())
    dispatch(setCurrentConsultantSearched(consultantToSearch))
    dispatch(clearCurrentConsultantToSearch())
  };

  return (
    <IconButton onClick={handleClick}>
      <PersonSearchIcon />
    </IconButton>
  );
}
