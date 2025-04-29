"use client";

import {useState, useEffect} from "react";
import axios from "axios";
import {SpeedTestChartData, SpeedTestResult, SpeedTestSummaryResult} from "@/types/speedTest"
import SpeedTestChart from "@/components/SpeedTestChart";

export default function Home() {
  const [latestSpeedTest, setLatestSpeedTest] = useState<SpeedTestResult | null>(null);
  const [speedTests, setSpeedTests] = useState<SpeedTestChartData[]>([]);
  const [summaryStats, setSummaryStats] = useState<SpeedTestSummaryResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    const fetchLatestSpeedTest = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/speed-tests/latest`);
        setLatestSpeedTest(response.data);
      } catch (err: unknown) {
          console.error("Error fetching speed test:", err)
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
            console.error("Error fetching speed tests:", err)
            handleError(err);
        }
    };

    const fetchSummaryStats = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/speed-tests/summary`);
            setSummaryStats(response.data);
        } catch (err: unknown) {
            console.error("Error fetching speed test summary:", err)
            handleError(err);
        }
    }

    const handleError = (err: unknown) => {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail ?? "Failed to fetch speed test data.");
      } else if (err instanceof Error) {
          setError(err.message);
      } else {
          setError("An unknown error occurred");
      }
  }

    fetchLatestSpeedTest();
    fetchSpeedTests();
    fetchSummaryStats();
  }, [API_URL]);

  const formatDate = (date: Date): string => {
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (error) return <p className="text-red-500 p-6">{error}</p>;
  if (!latestSpeedTest) return <p className="p-6">Loading latest speed test...</p>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Internet Speed Tracker</h1>

      {/*  Summary Section */}
      {summaryStats.length > 0 ? (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Speed Test Summary</h2>
        <div className="grid grid-cols-1 gap-6">
          {summaryStats.map((stats) => (
            <div key={stats.time_of_day ?? 'ALL'} className="border rounded-md p-4 mb-2 bg-yellow-100/70 dark:bg-amber-600/6">
              <h3 className="font-bold mb-2">
                {stats.time_of_day
                  ? `Summary (${stats.time_of_day})`
                  : "Summary (All Times)"}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">Download (Mbps)</p>
                  <p className="text-base">Avg: <span className="font-bold">{stats.avg_download_speed.toFixed(2)}</span></p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Max: {stats.max_download_speed.toFixed(2)}, Min: {stats.min_download_speed.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">Upload (Mbps)</p>
                  <p className="text-base">Avg: <span className="font-bold">{stats.avg_upload_speed.toFixed(2)}</span></p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Max: {stats.max_upload_speed.toFixed(2)}, Min: {stats.min_upload_speed.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">Latency (ms)</p>
                  <p className="text-base">Avg: <span className="font-bold">{stats.avg_latency.toFixed(2)}</span></p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Max: {stats.max_latency.toFixed(2)}, Min: {stats.min_latency.toFixed(2)}</p>
                </div>
              </div>
              <div className="text-sm text-gray-700 dark:text-gray-300">
                <p><strong>Tests Count:</strong> {stats.test_count}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    ) : (
      <p>Loading summary...</p>
    )}


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
      <p><strong>Test Time:</strong> {new Date(latestSpeedTest.timestamp).toLocaleString()}</p>
      <p><strong>Server:</strong> {latestSpeedTest.server.name}</p>
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
