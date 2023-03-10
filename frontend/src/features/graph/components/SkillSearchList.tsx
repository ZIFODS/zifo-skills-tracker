import * as React from "react";
import { Stack, Paper, Box, Typography, IconButton } from "@mui/material";
import { useEffect } from "react";
import { SkillSearchElement } from "../types";
import { categoryMap } from "../../../utils/skillCategories";
import ClearIcon from "@mui/icons-material/Clear";
import { useGetSkill } from "../api/getSkill";

interface SearchListProps {
  skillSearch: SkillSearchElement[];
  setSkillSearch: React.Dispatch<React.SetStateAction<SkillSearchElement[]>>;
}

/**
 * Component displaying list of skills to be searched
 */
export default function SkillSearchList({
  skillSearch,
  setSkillSearch,
}: SearchListProps) {
  /**
   * Get indices in search list where parenthesis matches supplied character.
   *
   * @param {string} char [ or ] character
   * @return {number[]} Indices of matching skills in search list
   */
  const getBracketIndexes = (char: string) => {
    return skillSearch
      .map((item: any, index: number) => ({ ...item, index }))
      .filter((item: any) => item.parenthesis == char)
      .map((item: any) => item.index);
  };

  // Get indices of open and closed parentheses
  let startBracketIdxs = getBracketIndexes("[");
  let endBracketIdxs = getBracketIndexes("]");

  // Update parenthesis indices when search list changes
  useEffect(() => {
    startBracketIdxs = getBracketIndexes("[");
    endBracketIdxs = getBracketIndexes("]");
  }, [skillSearch]);

  // Automatically scroll to bottom when search list updated
  const searchListScrollRef = React.useRef<null | HTMLDivElement>(null);
  const scrollToBottom = () => {
    searchListScrollRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => {
    scrollToBottom();
  }, [skillSearch]);

  let open = false;

  return (
    <Box
      sx={{
        height: 0,
        display: "flex",
        flexGrow: 1,
        overflowY: "scroll",
      }}
    >
      <Stack sx={{ flex: 1 }} spacing={1}>
        {skillSearch.map(function (rule: any, j: number) {
          // Determine if bracket is open
          if (rule.parenthesis === "[") {
            open = true;
          }
          if (rule.parenthesis === "]") {
            open = false;
          }

          // If bracket is closed return node normally
          if (!open && !endBracketIdxs.includes(j)) {
            return (
              <Stack spacing={1} ref={searchListScrollRef}>
                {rule.operator !== "" &&
                  (endBracketIdxs.map((idx: number) => idx + 1).includes(j) ||
                    j !== 0) && <SearchOperator operator={rule.operator} />}
                <SkillSearchElementBox
                  name={rule.name}
                  setSkillSearch={setSkillSearch}
                />
              </Stack>
            );
          }

          // If bracket is open then it should be wrapped in yellow paper
          // Nothing should be returned until either last node or closed parenthesis
          else if (endBracketIdxs.includes(j) || j === skillSearch.length - 1) {
            let startBracketIdx = startBracketIdxs[endBracketIdxs.indexOf(j)];
            if (startBracketIdx === undefined) {
              startBracketIdx = startBracketIdxs.slice(-1)[0];
            }
            const nodesInParentheses = skillSearch.filter(function (
              rule: any,
              k: number
            ) {
              return k >= startBracketIdx && k <= j;
            });
            return (
              <Stack spacing={1}>
                <SearchOperator
                  operator={skillSearch[startBracketIdx].operator}
                />
                <Paper sx={{ p: 1, py: 1.5, backgroundColor: "#e6d4aa" }}>
                  <Stack spacing={1}>
                    {nodesInParentheses.map(function (rule: any, k: number) {
                      return (
                        <Stack spacing={1} ref={searchListScrollRef}>
                          {rule.operator !== "" && k !== 0 && (
                            <SearchOperator operator={rule.operator} />
                          )}
                          <SkillSearchElementBox
                            name={rule.name}
                            setSkillSearch={setSkillSearch}
                          />
                        </Stack>
                      );
                    })}
                  </Stack>
                </Paper>
              </Stack>
            );
          }
        })}
      </Stack>
    </Box>
  );
}

interface SearchOperatorProps {
  operator: string;
}

/**
 * Box to display bitwise operator in search list
 */
function SearchOperator({ operator }: SearchOperatorProps) {
  return (
    <Typography variant="subtitle2" sx={{ px: 1, fontWeight: "bold" }}>
      {operator}
    </Typography>
  );
}

interface SkillSearchElementProps {
  name: string;
  setSkillSearch: React.Dispatch<React.SetStateAction<SkillSearchElement[]>>;
}

/**
 * Box to display skill group and name in search list
 */
function SkillSearchElementBox({
  name,
  setSkillSearch,
}: SkillSearchElementProps) {
  const { data } = useGetSkill({ name: name });
  const category = data?.category;

  // Clicking remove button
  const handleClick = () => {
    setSkillSearch((prev) => prev.filter((item) => item.name !== name));
  };

  return (
    <Paper>
      <Stack direction="row" sx={{ height: "100%" }}>
        <Typography
          sx={{
            backgroundColor: categoryMap[category]?.color,
            px: 1.5,
            py: 0.5,
            fontSize: 14,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          {categoryMap[category]?.displayName}
        </Typography>
        <Stack
          sx={{ display: "flex", flexGrow: 1 }}
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography sx={{ pl: 2, fontSize: 14 }}>{name}</Typography>
          <IconButton sx={{ my: 0, mx: 0.5 }} onClick={handleClick}>
            <ClearIcon sx={{ fontSize: 18 }} />
          </IconButton>
        </Stack>
      </Stack>
    </Paper>
  );
}
