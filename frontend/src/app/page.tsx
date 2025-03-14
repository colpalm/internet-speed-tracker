"use client";

import {useState, useEffect} from "react";
import axios from "axios";
import { SpeedTestResult } from "@/types/speedTest"

export default function Home() {
  const [speedTest, setSpeedTest] = useState<SpeedTestResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    (async () => {
      try {
        const response = await axios.get(`${API_URL}/api/speed-tests/latest`);
        setSpeedTest(response.data);
      } catch (err: unknown) {
          console.error("Error fetching speed test:", err)

          if (axios.isAxiosError(err)) {
              setError(err.response?.data?.detail || "Failed to fetch speed test data.");
          } else if (err instanceof Error) {
              setError(err.message);
          } else {
              setError("An unknown error occurred");
          }
      }
    })();
  }, [API_URL]);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!speedTest) return <p>Loading latest speed test...</p>;

  return (
      <div className="p-6">
        <h1 className="text-2xl font-bold">Internet Speed Tracker</h1>
        <h2 className="text-lg mt-4">Latest Speed Test Result</h2>
        <p><strong>Download Speed:</strong> {speedTest.download_speed} Mbps</p>
        <p><strong>Upload Speed:</strong> {speedTest.upload_speed} Mbps</p>
        <p><strong>Latency:</strong> {speedTest.latency} ms</p>
        <p><strong>Test Time:</strong> {new Date(speedTest.timestamp).toLocaleString()}</p>
        <p><strong>Server:</strong> {speedTest.server.name} (ID: {speedTest.server.id})</p>
      </div>
  );
}
