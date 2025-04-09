import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';
import { SpeedTestChartData } from "@/types/speedTest";

interface SpeedTestChartProps {
    data: SpeedTestChartData[];
}

const SpeedTestChart: React.FC<SpeedTestChartProps> = ({ data }) => {
    return (
        <div className="w-full h-[400px] mt-6">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    data={data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        dataKey="formatted_date"
                        tickMargin={10}
                    />
                    <YAxis
                        label={{
                            value: "Speed (Mbps)",
                            angle: -90,
                            position: "insideLeft",
                            style: { textAnchor: "middle" }
                        }}
                    />
                    <Tooltip />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="download_speed"
                        name="Download Speed"
                        stroke="#8884d8"
                        activeDot={{ r: 8 }}
                        strokeWidth={2}
                    />
                    <Line
                        type="monotone"
                        dataKey="upload_speed"
                        name="Upload Speed"
                        stroke="#82ca9d"
                        activeDot={{ r: 8 }}
                        strokeWidth={2}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default SpeedTestChart;