"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleUpload = async () => {
    if (!file) return alert("Select file");

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const blob = await res.blob();

    const url = window.URL.createObjectURL(blob);
    router.push(`/result?file=${encodeURIComponent(url)}`);

    setLoading(false);
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1 className="text-3xl font-bold">AI Resume Converter</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="border p-2"
      />

      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {loading ? "Processing..." : "Upload & Convert"}
      </button>
    </main>
  );
}