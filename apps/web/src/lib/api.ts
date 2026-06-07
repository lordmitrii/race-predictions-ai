export type DriverPrediction = {
  driver: string;
  podium_probability: number;
  points_probability: number;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function getPredictions(): Promise<DriverPrediction[]> {
  const res = await fetch(`${API_BASE_URL}/predictions`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch predictions");
  }

  return res.json();
}