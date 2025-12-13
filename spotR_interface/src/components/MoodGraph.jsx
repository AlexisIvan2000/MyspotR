import { useEffect, useState } from "react";
import { getMoodAnalysis } from "../services/spotify_api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function MoodGraph() {
  const [mood, setMood] = useState(null);

  useEffect(() => {
    getMoodAnalysis().then((res) => {
      const data = res.data.timeline.map((item, index) => ({
        index,
        score: item.score,
      }));
      setMood({ ...res.data, chartData: data });
    });
  }, []);

  if (!mood) return <p>Loading mood...</p>;

  return (
    <div className="card">
      <h2>Mood Evolution</h2>
      <p>
        Current mood: <strong>{mood.label}</strong>
      </p>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={mood.chartData}>
          <XAxis dataKey="index" />
          <YAxis domain={[-3, 3]} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#1db954"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="mood-summary">
        <p>
          Day mood: <strong>{mood.by_period?.day}</strong>
        </p>
        <p>
          Night mood: <strong>{mood.by_period?.night}</strong>
        </p>
      </div>
    </div>
  );
}
