import React from "react";
import { Typography } from "@mui/material";

import { ErrorProps } from "../types/types";

const ErrorMessage: React.FC<ErrorProps> = ({ error }) => {
  return (
    <Typography color="error" gutterBottom>
      {error}
    </Typography>
  );
};

export default ErrorMessage;
