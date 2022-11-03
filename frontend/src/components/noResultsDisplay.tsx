import React from 'react'
import {Stack, Typography} from "@mui/material"

/**
 * Message displayed when search returns no results
 */
export default function NoResultsDisplay() {
  return(
    <Stack spacing={5}>
      <Typography variant="h4" sx={{color: "#808080"}}>
      Your search did not return any results.
      </Typography>
      <Typography variant="h4" sx={{color: "#808080"}}>
      Try again with a different set of skills.
      </Typography>
    </Stack>
  )
}