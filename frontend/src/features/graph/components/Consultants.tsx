import React from "react";
import {
  Stack,
  Typography,
  Paper,
  Box,
  IconButton,
  Autocomplete,
  TextField,
} from "@mui/material";
import PersonSearchIcon from "@mui/icons-material/PersonSearch";
import { useGetAllConsultants } from "../api/getAllConsultants";
import { consultantInitials } from "../utils/initials";
import * as d3 from "d3";

interface ConsultantsProps {
  consultantSearch: string | null;
  setConsultantSearch: React.Dispatch<React.SetStateAction<string | null>>;
  setConsultantApplyClicked: React.Dispatch<React.SetStateAction<boolean>>;
  displayedConsultants: string[];
  hoveredConsultants: string[];
}

/**
 * Consultants section
 */
export default function Consultants({
  consultantSearch,
  setConsultantSearch,
  setConsultantApplyClicked,
  displayedConsultants,
  hoveredConsultants,
}: ConsultantsProps) {
  const allConsultantsData = useGetAllConsultants().data?.items;
  const allConsultants = allConsultantsData
    ? allConsultantsData.map((consultant: any) => consultant.name)
    : [];

  const handleAutocompleteChange = (event: any, value: string | null) => {
    if (value != null) {
      setConsultantSearch(value);
    }
  };

  const handleSearchClick = () => {
    setConsultantApplyClicked(true);
  };

  return (
    <Paper
      sx={{
        border: "2px solid black",
        p: 2.5,
        backgroundColor: "#e5e5e5",
        display: "flex",
        flexGrow: 1,
      }}
    >
      <Stack spacing={2}>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
            <Typography
              variant="h5"
              sx={{ color: "#1f226a", fontWeight: "bold" }}
            >
              Consultants
            </Typography>
          </Box>
          <Box sx={{ flexGrow: 1 }} />
        </Stack>
        <Stack direction="row" spacing={1}>
          <Autocomplete
            disablePortal
            id="combo-box-demo"
            options={allConsultants}
            value={consultantSearch}
            onChange={handleAutocompleteChange}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Consultant name"
                variant="standard"
                sx={{ width: "10vw" }}
                InputLabelProps={{
                  style: { fontSize: 14, margin: 0, padding: 0 },
                }}
              />
            )}
          />
          <IconButton onClick={handleSearchClick}>
            <PersonSearchIcon />
          </IconButton>
        </Stack>
        <Stack spacing={2} sx={{ overflow: "scroll", py: 2 }}>
          {displayedConsultants.map(function (name: string) {
            const initials = consultantInitials(name);
            return (
              <Paper
                sx={{
                  px: 1,
                  py: 0.5,
                  backgroundColor: d3.schemePaired[0] + "70",
                  opacity: hoveredConsultants.includes(name)
                    ? 1
                    : hoveredConsultants.length > 0
                    ? 0.1
                    : 1,
                }}
              >
                <Stack
                  direction="row"
                  spacing={3}
                  justifyContent="flex-start"
                  alignItems="center"
                >
                  <Typography sx={{ fontSize: 15, fontWeight: "bold" }}>
                    {initials}
                  </Typography>
                  <Typography sx={{ fontSize: 15 }}>{name}</Typography>
                </Stack>
              </Paper>
            );
          })}
        </Stack>
      </Stack>
    </Paper>
  );
}
