import React, { useState } from "react";
import {
  TextField,
  Button,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import api from "../../api";

function ProjectFilter({ onApplyFilters, regions, ministries }) {
  const [filters, setFilters] = useState({
    region: "",
    ministry: "",
    status: "",
    searchTerm: "",
  });

  const handleChange = (event) => {
    setFilters({
      ...filters,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onApplyFilters(filters);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth variant="outlined">
            <InputLabel id="region-label">Region</InputLabel>
            <Select
              labelId="region-label"
              id="region-select"
              name="region"
              value={filters.region}
              onChange={handleChange}
              label="Region"
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {regions.map((region) => (
                <MenuItem key={region.id} value={region.id}>
                  {region.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth variant="outlined">
            <InputLabel id="ministry-label">Ministry</InputLabel>
            <Select
              labelId="ministry-label"
              id="ministry-select"
              name="ministry"
              value={filters.ministry}
              onChange={handleChange}
              label="Ministry"
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {ministries.map((ministry) => (
                <MenuItem key={ministry.id} value={ministry.id}>
                  {ministry.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth variant="outlined">
            <InputLabel id="status-label">Status</InputLabel>
            <Select
              labelId="status-label"
              id="status-select"
              name="status"
              value={filters.status}
              onChange={handleChange}
              label="Status"
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              <MenuItem value={"In Progress"}>In Progress</MenuItem>
              <MenuItem value={"Completed"}>Completed</MenuItem>
              <MenuItem value={"Delayed"}>Delayed</MenuItem>
              <MenuItem value={"Not Started"}>Not Started</MenuItem>
              {/* Add more status options as needed */}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            variant="outlined"
            label="Search"
            name="searchTerm"
            value={filters.searchTerm}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={12}>
          <Button type="submit" variant="contained" color="primary">
            Apply Filters
          </Button>
        </Grid>
      </Grid>
    </form>
  );
}

export default ProjectFilter;