import React from "react";
import { Box, Typography, Divider } from "@mui/material";

import { TranscriptsProps } from "../types/types";

const Transcripts: React.FC<TranscriptsProps> = ({
  transcriptRef,
  transcripts,
  currentTime,
}) => {
  const formatTime = (start: number) => {
    const minutes = Math.floor(start / 60);
    const seconds = Math.floor(start % 60)
      .toString()
      .padStart(2, "0");
    return `${minutes}:${seconds}`;
  };

  return (
    <div>
      <Box
        ref={transcriptRef}
        sx={{
          border: "1px solid #ccc",
          borderRadius: 2,
          overflowY: "auto",
          maxHeight: "300px",
          p: 2,
          backgroundColor: "#121212",
          color: "white",
        }}
      >
        <Typography variant="h6" gutterBottom>
          Transcripts:
        </Typography>
        <Divider sx={{ mb: 2 }} />
        {transcripts.map((transcript, index) => (
          <Typography
            key={index}
            sx={{
              mb: 1,
              fontSize: "14px",
              lineHeight: 1.6,
              backgroundColor:
                currentTime >= transcript.start &&
                currentTime < transcript.start + transcript.duration
                  ? "#333333"
                  : "transparent",
              borderRadius: "4px",
              padding: "4px",
            }}
          >
            <strong>{formatTime(transcript.start)}</strong>: {transcript.text}
          </Typography>
        ))}
      </Box>
    </div>
  );
};

export default Transcripts;
