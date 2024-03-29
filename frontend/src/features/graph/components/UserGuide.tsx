import React from "react";
import { Paper, Typography, Box, Stack, IconButton } from "@mui/material";
import PersonSearchIcon from "@mui/icons-material/PersonSearch";
import ClearIcon from "@mui/icons-material/Clear";
import searchBarImage from "../../../assets/search-bar.png";
import andOrToggleAndSelectedImage from "../../../assets/and-or-toggle-and-selected.png";
import andOrToggleOrSelectedImage from "../../../assets/and-or-toggle-or-selected.png";
import bracketedQueryImage from "../../../assets/bracketed-query.png";
import bracketToggleOpenSelectedImage from "../../../assets/bracket-toggle-open-selected.png";
import bracketToggleClosedSelectedImage from "../../../assets/bracket-toggle-closed-selected.png";
import clearApplyImage from "../../../assets/clear-apply.png";
import skillImage from "../../../assets/skill.png";
import consultantSearchImage from "../../../assets/consultants-search.png";
import categoriesImage from "../../../assets/categories.png";
import consultantSectionImage from "../../../assets/consultants-section.png";
import nodeHoverImage from "../../../assets/node-hover.png";
import consultantHoverImage from "../../../assets/consultants-hover.png";

interface UserGuideProps {
  setUserGuideOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

/**
 * User guide section
 */
export default function UserGuide({ setUserGuideOpen }: UserGuideProps) {
  const handleCloseClick = () => {
    setUserGuideOpen(false);
  };

  return (
    <Paper
      elevation={8}
      sx={{
        border: "2px solid black",
        backgroundColor: "#e5e5e5",
        fontWeight: "bold",
        p: 2.5,
        height: "92%",
        width: "94%",
        overflowY: "scroll",
      }}
    >
      <Stack spacing={4}>
        <Stack direction="row">
          <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
            <Typography
              variant="h5"
              sx={{ fontWeight: "bold", color: "#1f226a" }}
            >
              User Guide
            </Typography>
          </Box>
          <Box sx={{ display: "flex", flexGrow: 1 }} />
          <IconButton onClick={handleCloseClick}>
            <ClearIcon sx={{ fontSize: 30, color: "black" }} />
          </IconButton>
        </Stack>
        <Stack spacing={5}>
          <Typography>
            <BoldInLineText text="1." /> You can either search for a set of
            skills in the <BoldInLineText text="Skills" /> section or an
            individual Consultant in the <BoldInLineText text="Consultants" />{" "}
            section.
          </Typography>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="2. a." /> To search with skills, type the
              name of a skill into the search bar at the top of the{" "}
              <BoldInLineText text="Skills" /> section and click{" "}
              <BoldInLineText text="+" /> to add it to the search query.
            </Typography>
            <Box>
              <img src={searchBarImage} width="300" height="100%" />
            </Box>
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="b." /> If you're adding more than one skill
              to the query, use the <BoldInLineText text="AND/OR" /> toggle
              buttons to define the relationship between skills.
            </Typography>
            <Typography>
              Select either <BoldInLineText text="AND" /> or{" "}
              <BoldInLineText text="OR" /> when adding a skill to define the
              relationship between it and the previous skill.
            </Typography>
            <Typography>
              <BoldInLineText text="AND" /> is automatically selected as the
              default relationship.
            </Typography>
            <Stack direction="row" spacing={3}>
              <img
                src={andOrToggleAndSelectedImage}
                width="100"
                height="100%"
              />
              <img src={andOrToggleOrSelectedImage} width="100" height="100%" />
            </Stack>
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="c." /> You can use brackets to bundle
              together groups of skills.
            </Typography>
            <Typography>
              For example, you might want to find a Consultant that knows either
              Python or R Studio but also knows either French or German.
            </Typography>
            <img src={bracketedQueryImage} width="300" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="d." /> If a skill belongs at the start of a
              set of brackets then you should select the open bracket toggle
              button <BoldInLineText text="[" /> and add the skill.
            </Typography>
            <Typography>
              The <BoldInLineText text="AND/OR" /> relationship you define at
              the start of a set of brackets will apply between the previous and
              current set of brackets.
            </Typography>
            <Typography>
              To close a set of brackets, add the final skill with the close
              bracket toggle button <BoldInLineText text="]" /> selected.
            </Typography>
            <Stack direction="row" spacing={3}>
              <img
                src={bracketToggleOpenSelectedImage}
                width="70"
                height="100%"
              />
              <img
                src={bracketToggleClosedSelectedImage}
                width="70"
                height="100%"
              />
            </Stack>
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="e." /> To visualise the results of your
              skill search query, click the <BoldInLineText text="APPLY" />{" "}
              button.
            </Typography>
            <Typography>
              You can clear the skill search query at any point using{" "}
              <BoldInLineText text="CLEAR" />.
            </Typography>
            <Typography>
              Alternatively, you can remove a single skill from the list using
              the <BoldInLineText text="x" /> button on the skill itself.
            </Typography>
            <Stack direction="row" alignItems="center" spacing={3}>
              <img src={clearApplyImage} width="300" height="100%" />
              <img src={skillImage} width="300" height="100%" />
            </Stack>
          </Stack>
          <Typography>
            <BoldInLineText text="f." /> Applying a skill search will result in
            the graph displaying only the categories associated with skills in
            the search query.
          </Typography>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="8." /> To search by Consultant, type the
              Consultant's name into the search bar in the{" "}
              <BoldInLineText text="Consultants" /> section and click{" "}
              <PersonSearchIcon />
            </Typography>
            <img src={consultantSearchImage} width="210" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="9." />
              Use the <BoldInLineText text="Categories" /> section to select and
              visualise other categories or click the{" "}
              <BoldInLineText text="SHOW ALL" /> or{" "}
              <BoldInLineText text="HIDE ALL" /> buttons.
            </Typography>
            <img src={categoriesImage} width="300" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="10." /> All Consultants returned by the
              applied search will have their full names displayed in the{" "}
              <BoldInLineText text="Consultants" /> section.
            </Typography>
            <img src={consultantSectionImage} width="200" height="100%" />
          </Stack>
          <Stack spacing={1}>
            <Typography>
              <BoldInLineText text="11." /> Hovering over a Consultant or skill
              node will highlight any connected nodes and connected Consultants'
              full names in the <BoldInLineText text="Consultants" /> section.
            </Typography>
            <Stack direction="row" spacing={3}>
              <Box sx={{ border: "1px solid black", width: 200, height: 260 }}>
                <img src={nodeHoverImage} width="200" height="260" />
              </Box>
              <img src={consultantHoverImage} width="140" height="300" />
              <Box sx={{ flexGrow: 1 }} />
            </Stack>
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}

interface BoldInLineTextProps {
  text: string;
}

function BoldInLineText({ text }: BoldInLineTextProps) {
  return (
    <Box fontWeight="bold" display="inline">
      {text}
    </Box>
  );
}
