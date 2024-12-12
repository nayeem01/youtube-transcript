import React from "react";
import { Box, Button, TextField, CircularProgress } from "@mui/material";

import { UrlProps } from "../types/types";

const Url: React.FC<UrlProps> = ({ url, setUrl, handleSubmit, loading }) => {
  return (
    <Box display="flex" alignItems="center" gap={2} mb={3}>
      <TextField
        label="Url"
        variant="outlined"
        fullWidth
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <Button
        variant="contained"
        color="primary"
        size="large"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : "Submit"}
      </Button>
    </Box>
  );
};

export default Url;
