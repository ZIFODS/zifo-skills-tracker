import React from "react";
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from "@mui/material";

export default function GroupSelect() {
  const groups = [
    "Consultant",
    "ScienceApps",
    "Services",
    "Methodologies",
    "Process",
    "Other_Products",
    "Regulatory",
    "Data_Management",
    "Languages",
    "programming",
    "Miscellaneous",
    "Infrastructure"
  ]

  const [selectedGroup, setSelectedGroup] = React.useState("")

  const handleChange = (event: SelectChangeEvent) => {
    setSelectedGroup(event.target.value)
  }

    return(
      <FormControl variant="standard" sx={{minWidth:150}}>
        <InputLabel sx={{fontSize: 14}} id="demo-simple-select-standard-label">Select group</InputLabel>
        <Select
          value={selectedGroup}
          onChange={handleChange}
          label="Select group"
          sx={{fontSize: 14}}
        >
          {groups.map(group => {
            console.log(group)
            return(
            <MenuItem value={group}>{group}</MenuItem>
            )
          })}
        </Select>
      </FormControl>
    )
}