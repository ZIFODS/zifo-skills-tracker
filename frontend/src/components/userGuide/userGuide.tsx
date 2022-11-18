import React from "react";
import { Paper, Typography, Box, Stack, IconButton } from "@mui/material";
import UserGuideHeader from "./userGuideHeader";
import BoldInlineText from "./boldInlineText";

/**
 * User guide section
 */
export default function UserGuide() {

  return (
    <Paper
      elevation={8}
      sx={{
        border: "1px solid black",
        backgroundColor: "#e5e5e5", 
        fontWeight:"bold",
        p: 2.5,
        height: "92%",
        width: "94%",
        overflowY: "scroll"
      }}
    >
      <Stack spacing={4}>
        <UserGuideHeader/>
        <Stack spacing={5}>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="1."/> Type the name of a skill into the search bar at the top of the <BoldInlineText text="Search"/> section and click <BoldInlineText text="+"/> to add it to the search query.
            </Typography>
            <img src={require("../../images/search-bar.png")} width="300" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="2."/> If you're adding more than one skill to the query, use the <BoldInlineText text="AND/OR"/> toggle buttons to define the relationship between skills.
            </Typography>
            <Typography>
              Select either <BoldInlineText text="AND"/> or <BoldInlineText text="OR"/> when adding a skill to define the relationship between it and the previous skill.
            </Typography>
            <Typography>
              <BoldInlineText text="AND"/> is automatically selected as the default relationship.
            </Typography>
            <Stack direction="row" spacing={3}>
              <img src={require("../../images/and-or-toggle-and-selected.png")} width="100" height="100%" />
              <img src={require("../../images/and-or-toggle-or-selected.png")} width="100" height="100%" />
            </Stack>
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="3."/> You can use brackets to bundle together groups of skills.
            </Typography>
            <Typography>
              For example, you might want to find a consultant that knows either Python or R Studio but also knows either French or German.
            </Typography>
            <img src={require("../../images/bracketed-query.png")} width="300" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="4."/> If a skill belongs at the start of a set of brackets then you should select the open bracket toggle button <BoldInlineText text="["/> and add the skill.
            </Typography>
            <Typography>
              The <BoldInlineText text="AND/OR"/> relationship you define at the start of a set of brackets will apply between the previous and current set of brackets.
            </Typography>
            <Typography>
              To close a set of brackets, add the final skill with the close bracket toggle button <BoldInlineText text="]"/> selected.
            </Typography>
            <Stack direction="row" spacing={3}>
              <img src={require("../../images/bracket-toggle-open-selected.png")} width="70" height="100%" />
              <img src={require("../../images/bracket-toggle-closed-selected.png")} width="70" height="100%" />
            </Stack>
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="5."/> To visualise the results of your search query, click the <BoldInlineText text="APPLY"/> button.
            </Typography>
            <Typography>
              You can clear the search query and current results at any point using <BoldInlineText text="CLEAR"/>.
            </Typography>
            <Typography>
              Alternatively, you can remove a single skill from the list using the <BoldInlineText text="x"/> button on the skill itself.
            </Typography>
            <Stack direction="row" alignItems="center" spacing={3}>
              <img src={require("../../images/clear-apply.png")} width="300" height="100%" />
              <img src={require("../../images/skill.png")} width="300" height="100%" />
            </Stack>
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="6."/> Applying a search will result in the graph displaying only the categories associated with skills in the search query.
            </Typography>
            <Typography>
              Use the <BoldInlineText text="Categories"/> section to select and visualise other categories or click the <BoldInlineText text="SHOW ALL"/> or <BoldInlineText text="HIDE ALL"/> buttons.
            </Typography>
            <img src={require("../../images/categories.png")} width="300" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="7."/> All consultants returned by the applied search will have their full names displayed in the <BoldInlineText text="Consultants"/> section.
            </Typography>
            <img src={require("../../images/consultants-section.png")} width="180" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInlineText text="8."/> Hovering over a consultant or skill node will highlight any connected nodes and connected consultants' full names in the <BoldInlineText text="Consultants"/> section.
            </Typography>
            <Stack direction="row" spacing={3}>
              <img src={require("../../images/node-hover.png")} width="350" height="100%" />
              <img src={require("../../images/consultants-hover.png")} width="140" height="100%" />
              <Box sx={{flexGrow: 1}}/>
            </Stack>
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}