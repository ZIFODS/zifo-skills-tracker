import React, { useEffect, useState } from "react";
import { Stack, Typography, Paper, Box } from "@mui/material";
import { consultantInitials } from "../graph/utils";
import * as d3 from "d3";
import { useAppSelector } from "../../app/hooks";
import { selectLinkedConsultantsOnHover, selectIsHovered } from "../graph/hoveredNodeSlice";
import { GraphNode } from "../graph/graphSlice";

interface IConsultantName {
  name: string;
}

/**
 * Box with individual Consultant's initials and name.
 */
export default function ConsultantName({name}: IConsultantName) {

  const initials = consultantInitials(name)

  let linkedConsultantsOnHover = useAppSelector(selectLinkedConsultantsOnHover)
  const isHovered = useAppSelector(selectIsHovered)

  let isCurrentConsultantHovered = false;
  const [opacity, setOpacity] = useState(1)

  useEffect(() => {
    isCurrentConsultantHovered = linkedConsultantsOnHover.includes(name);
    if (isHovered && !isCurrentConsultantHovered) {
      setOpacity(0.1)
    }
    else {
      setOpacity(1)
    }
  }, [isHovered])

  return (
    <Paper sx={{px: 1, py: 0.5, backgroundColor: d3.schemePaired[0] + "70", opacity: opacity}}>
      <Stack direction="row" spacing={3} justifyContent="flex-start" alignItems="center">
        <Typography sx={{fontSize: 15, fontWeight: "bold"}}>
          {initials}
        </Typography>
        <Typography sx={{fontSize: 15}}>
          {name}
        </Typography>
      </Stack>
    </Paper>
  );
}
