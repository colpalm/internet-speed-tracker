export interface SpeedTestResult {
  timestamp: string;
  download_speed: number;
  upload_speed: number;
  latency: number;
  time_of_day: string;
  server: {name: string, url: string};
}

export interface SpeedTestChartData extends SpeedTestResult {
  formatted_date: string;
}

export interface SpeedTestSummaryResult {
  time_of_day: string;
  avg_download_speed: number;
  max_download_speed: number;
  min_download_speed: number;
  avg_upload_speed: number;
  max_upload_speed: number;
  min_upload_speed: number;
  avg_latency: number;
  max_latency: number;
  min_latency: number;
  test_count: number;
}