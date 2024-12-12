import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    API_IP: process.env.API_IP,
  },
};

export default nextConfig;
