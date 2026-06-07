import { getPredictions } from "@/lib/api";

export default async function Home() {
  const predictions = await getPredictions();

  return (
    <main className="mx-auto max-w-3xl p-8">
      <h1 className="text-3xl font-bold">Pitwall AI</h1>
      <p className="mt-2 text-gray-600">
        Explainable race prediction platform.
      </p>

      <section className="mt-8 space-y-4">
        {predictions.map((prediction) => (
          <div
            key={prediction.driver}
            className="rounded-xl border p-4 shadow-sm"
          >
            <h2 className="text-xl font-semibold">{prediction.driver}</h2>
            <p>
              Podium probability:{" "}
              {(prediction.podium_probability * 100).toFixed(1)}%
            </p>
            <p>
              Points probability:{" "}
              {(prediction.points_probability * 100).toFixed(1)}%
            </p>
          </div>
        ))}
      </section>
    </main>
  );
}