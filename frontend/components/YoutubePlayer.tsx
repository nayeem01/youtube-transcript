import React from "react";
import { Typography, Paper } from "@mui/material";

const YoutubePlayer = () => {
  return (
    <Paper elevation={3} sx={{ p: 2, mb: 3, backgroundColor: "#f0f0f0" }}>
      <Typography variant="h6" gutterBottom>
        YouTube Video Player
      </Typography>
      <div id="youtube-player" style={{ width: "100%", height: "360px" }}></div>
    </Paper>
  );
};

export default YoutubePlayer;
