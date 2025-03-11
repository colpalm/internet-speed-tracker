export interface SpeedTestResult {
  timestamp: string;
  download_speed: number;
  upload_speed: number;
  latency: number;
  time_of_day: string;
  server: {id: number, name: string};
}