import React from "react";
import {
  Stack,
  Typography,
  Paper,
  Box,
  FormGroup,
  FormControlLabel,
  Checkbox,
  FormControl,
  Button,
} from "@mui/material";
import { useGetAllCategories } from "../api/getAllCategories";
import { categoryMap } from "../../../utils/skillCategories";

/**
 * Splits array of category names into chunks of defined size.
 *
 * @param {string[]} groups Array of category names
 * @return {string[][]} n array of m string array where m is chunk size.
 */
const categoriesIntoChunks = (categories: string[]) => {
  const chunkSize = 6;
  const chunkedCategories = [];
  for (let i = 0; i < categories.length; i += chunkSize) {
    chunkedCategories.push(categories.slice(i, i + chunkSize));
  }
  return chunkedCategories;
};

interface CategoriesProps {
  hiddenCategories: string[];
  setHiddenCategories: React.Dispatch<React.SetStateAction<string[]>>;
  searchedCategories: string[];
  filteredCategories: string[];
}

/**
 * Category filtering section
 */
export default function Categories({
  hiddenCategories,
  setHiddenCategories,
  searchedCategories,
  filteredCategories,
}: CategoriesProps) {
  const allCategories = useGetAllCategories().data?.items;
  const allCategoriesChunked =
    allCategories !== undefined ? categoriesIntoChunks(allCategories) : [];

  const handleHideAllClick = () => {
    setHiddenCategories(allCategories);
  };

  const handleShowAllClick = () => {
    setHiddenCategories([]);
  };

  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const category = event.target.name;
    if (category !== undefined) {
      // Clicking checked checkbox updates hidden groups with name
      if (!event.target.checked) {
        if (!hiddenCategories.includes(category)) {
          setHiddenCategories([...hiddenCategories, category]);
        }
      }
      // Clicking unchecked checkbox removes name from hidden groups list
      else {
        const hiddenCategoriesUpdated = hiddenCategories.filter(function (
          c: string
        ) {
          return c !== category;
        });
        setHiddenCategories(hiddenCategoriesUpdated);
      }
    }
  };

  return (
    <Paper
      sx={{ border: "2px solid black", p: 2.5, backgroundColor: "#e5e5e5" }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Box sx={{ borderBottom: "1px solid black", pb: 1, mb: 1 }}>
          <Typography
            variant="h5"
            sx={{ color: "#1f226a", fontWeight: "bold" }}
          >
            Categories
          </Typography>
        </Box>
        <Stack spacing={1} direction="row" justifyContent="flex-end">
          <Button
            variant="outlined"
            disabled={!searchedCategories.length}
            sx={{ p: 0.5, fontSize: 10 }}
            onClick={handleHideAllClick}
          >
            Hide all
          </Button>
          <Button
            variant="outlined"
            disabled={!searchedCategories.length}
            sx={{ p: 0.5, fontSize: 10 }}
            onClick={handleShowAllClick}
          >
            Show all
          </Button>
        </Stack>
      </Stack>
      <Stack direction="row" spacing={2}>
        {allCategoriesChunked.map(function (chunk: string[]) {
          return (
            <Stack sx={{ pt: 0.5 }}>
              {chunk.map(function (category: string) {
                return (
                  <FormControl component="fieldset" variant="outlined">
                    <FormGroup>
                      {searchedCategories.includes(category) ? (
                        <FormControlLabel
                          control={
                            <Checkbox
                              checked={
                                filteredCategories.includes(category) ||
                                !hiddenCategories.includes(category)
                              }
                              onChange={handleCheckboxChange}
                              sx={{ transform: "scale(0.8)", p: 0.5, pl: 1.5 }}
                            />
                          }
                          label={
                            <Typography sx={{ fontSize: 13 }}>
                              {categoryMap[category].displayName}
                            </Typography>
                          }
                          name={category}
                        />
                      ) : (
                        <FormControlLabel
                          disabled
                          control={
                            <Checkbox
                              disabled
                              checked={false}
                              onChange={handleCheckboxChange}
                              sx={{ transform: "scale(0.8)", p: 0.5, pl: 1.5 }}
                            />
                          }
                          label={
                            <Typography sx={{ fontSize: 13, color: "#808080" }}>
                              {categoryMap[category].displayName}
                            </Typography>
                          }
                          name={category}
                        />
                      )}
                    </FormGroup>
                  </FormControl>
                );
              })}
            </Stack>
          );
        })}
      </Stack>
    </Paper>
  );
}
