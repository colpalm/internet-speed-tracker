"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { SpeedTestChartData, SpeedTestResult, SpeedTestSummaryResult } from "@/types/speedTest";
import { TimeOfDay, TIME_OF_DAY_OPTIONS } from "@/types/timePeriods";
import SpeedTestChart from "@/components/SpeedTestChart";

export default function Home() {
  const [latestSpeedTest, setLatestSpeedTest] = useState<SpeedTestResult | null>(null);
  const [speedTests, setSpeedTests] = useState<SpeedTestChartData[]>([]);
  const [summaryStats, setSummaryStats] = useState<SpeedTestSummaryResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [selectedTimeOfDay, setSelectedTimeOfDay] = useState<TimeOfDay>(null);
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    const fetchLatestSpeedTest = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/speed-tests/latest`);
        setLatestSpeedTest(response.data);
      } catch (err: unknown) {
        console.error("Error fetching speed test:", err);
        handleError(err);
      }
    };

    const fetchSpeedTests = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/speed-tests?limit=10`);

        // Transform data for the chart
        const chartData: SpeedTestChartData[] = response.data.map((test: SpeedTestResult) => {
          const date = new Date(test.timestamp);
          return {
            timestamp: test.timestamp,
            formatted_date: formatDate(date),
            download_speed: test.download_speed,
            upload_speed: test.upload_speed,
            latency: test.latency,
          };
        });

        setSpeedTests(chartData);
      } catch (err: unknown) {
        console.error("Error fetching speed tests:", err);
        handleError(err);
      }
    };

    const fetchSummaryStats = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/speed-tests/summary`);
        setSummaryStats(response.data);
      } catch (err: unknown) {
        console.error("Error fetching speed test summary:", err);
        handleError(err);
      }
    };

    const handleError = (err: unknown) => {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail ?? "Failed to fetch speed test data.");
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    };

    fetchLatestSpeedTest();
    fetchSpeedTests();
    fetchSummaryStats();
  }, [API_URL]);

  const formatDate = (date: Date): string => {
    return date.toLocaleDateString() + " " + date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  // Stats for the selected time of day
  const getSelectedStats = (): SpeedTestSummaryResult | undefined => {
    return summaryStats.find(stats => stats.time_of_day === selectedTimeOfDay);
  };

  const selectedStats = getSelectedStats();

  if (error) return <p className="text-red-500 p-6">{error}</p>;
  if (!latestSpeedTest) return <p className="p-6">Loading latest speed test...</p>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Internet Speed Tracker</h1>

      {/* Time period selector */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          {TIME_OF_DAY_OPTIONS.map(option => (
            <button
              key={option.label}
              onClick={() => setSelectedTimeOfDay(option.value)}
              className={`px-2 py-1 rounded-lg transition-colors ${
                selectedTimeOfDay === option.value
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600"
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-xl mb-8">
        <h2 className="text-xl font-semibold mb-4">Summary Stats</h2>
        {selectedStats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Download Speed Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Download Speed</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Average</p>
                  <p className="text-xl font-bold">{selectedStats.avg_download_speed.toFixed(1)} Mbps</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Maximum</p>
                  <p className="text-xl font-bold text-green-600 dark:text-green-400">
                    {selectedStats.max_download_speed.toFixed(1)} Mbps
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Minimum</p>
                  <p className="text-xl font-bold text-red-600 dark:text-red-400">
                    {selectedStats.min_download_speed.toFixed(1)} Mbps
                  </p>
                </div>
              </div>
            </div>

            {/* Upload Speed Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Upload Speed</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Average</p>
                  <p className="text-xl font-bold">{selectedStats.avg_upload_speed.toFixed(1)} Mbps</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Maximum</p>
                  <p className="text-xl font-bold text-green-600 dark:text-green-400">
                    {selectedStats.max_upload_speed.toFixed(1)} Mbps
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Minimum</p>
                  <p className="text-xl font-bold text-red-600 dark:text-red-400">
                    {selectedStats.min_upload_speed.toFixed(1)} Mbps
                  </p>
                </div>
              </div>
            </div>

            {/* Latency Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Latency</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Average</p>
                  <p className="text-xl font-bold">{selectedStats.avg_latency.toFixed(1)} ms</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Maximum</p>
                  <p className="text-xl font-bold text-red-600 dark:text-red-400">
                    {selectedStats.max_latency.toFixed(1)} ms
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Minimum</p>
                  <p className="text-xl font-bold text-green-600 dark:text-green-400">
                    {selectedStats.min_latency.toFixed(1)} ms
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Latest Result Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Latest Speed Test Result</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-300">Download Speed</p>
            <p className="text-2xl font-bold text-blue-600 dark:text-blue-300">{latestSpeedTest.download_speed} Mbps</p>
          </div>
          <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-300">Upload Speed</p>
            <p className="text-2xl font-bold text-green-600 dark:text-green-300">{latestSpeedTest.upload_speed} Mbps</p>
          </div>
          <div className="p-4 bg-purple-50 dark:bg-purple-900 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-300">Latency</p>
            <p className="text-2xl font-bold text-purple-600 dark:text-purple-300">{latestSpeedTest.latency} ms</p>
          </div>
        </div>
        <div className="mt-4 text-sm text-gray-600 dark:text-gray-300">
          <p>
            <strong>Test Time:</strong> {new Date(latestSpeedTest.timestamp).toLocaleString()}
          </p>
          <p>
            <strong>Server:</strong> {latestSpeedTest.server.name}
          </p>
        </div>
      </div>

      {speedTests.length > 0 ? (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Speed Test History</h2>
          <SpeedTestChart data={speedTests} />
        </div>
      ) : (
        <p>Loading speed test history...</p>
      )}
    </div>
  );
}
