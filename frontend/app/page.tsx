"use client";

import { useState } from "react";
import { UploadCloud, FileText, Loader2, Download } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Select file");

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      alert("Upload failed");
      setLoading(false);
      return;
    }

    const blob = await res.blob();

    // 👉 create preview url
    const url = window.URL.createObjectURL(blob);
    setPreviewUrl(url);

    setLoading(false);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6 gap-6">
      
      {/* Upload Card */}
      <div className="w-full max-w-md backdrop-blur-xl bg-white/20 border border-white/30 shadow-2xl rounded-2xl p-8 flex flex-col items-center gap-6">

        <div className="text-center">
          <h1 className="text-3xl font-bold text-white">AI Resume Converter</h1>
          <p className="text-white/80 text-sm">
            Convert your resume into Apexon format instantly
          </p>
        </div>

        {/* Upload box */}
        <label className="w-full flex flex-col items-center justify-center border-2 border-dashed border-white/40 rounded-xl p-8 cursor-pointer hover:bg-white/10 transition">
          <UploadCloud className="text-white mb-2" size={36} />

          {file ? (
            <div className="flex items-center gap-2 text-white">
              <FileText size={18} />
              <span className="text-sm">{file.name}</span>
            </div>
          ) : (
            <span className="text-white/80 text-sm">
              Click or drag resume here
            </span>
          )}

          <input hidden type="file" onChange={(e) => setFile(e.target.files[0])} />
        </label>

        {/* Upload button */}
        <button
          onClick={handleUpload}
          className="w-full flex items-center justify-center gap-2 bg-white text-purple-600 font-semibold py-3 rounded-xl hover:scale-105 transition shadow-lg"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={18} />
              Processing...
            </>
          ) : (
            "Upload & Convert"
          )}
        </button>
      </div>

      {/* ⭐ Preview Section appears after upload */}
      {previewUrl && (
        <div className="w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden">
          
          {/* Preview */}
          <iframe src={previewUrl} className="w-full h-[700px]" />

          {/* Download button */}
          <div className="p-4 flex justify-center border-t">
            <a
              href={previewUrl}
              download="converted_resume.html"
              className="flex items-center gap-2 bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700"
            >
              <Download size={18} />
              Download Resume
            </a>
          </div>
        </div>
      )}
    </main>
  );
}