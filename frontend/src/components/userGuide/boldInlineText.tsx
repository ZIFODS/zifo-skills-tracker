import React from "react";
import {Box} from "@mui/material"

interface IBoldInlineText {
    text: string;
}

export default function BoldInlineText({text}: IBoldInlineText) {
  return(
    <Box fontWeight='bold' display='inline'>{text}</Box>
  )
}