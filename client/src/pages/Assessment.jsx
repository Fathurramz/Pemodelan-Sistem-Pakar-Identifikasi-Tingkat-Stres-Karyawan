import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import Footer from "../components/Footer";
import logoAplikasi from "../assets/logo-capstone.svg";

const Assessment = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Ambil data pertanyaan dari Backend
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/questions");
        if (!response.ok) {
          throw new Error("Gagal memuat daftar pertanyaan dari server.");
        }
        const data = await response.json();
        
        // Urutkan berdasarkan order_number
        const sorted = data.questions.sort((a, b) => a.order_number - b.order_number);
        setQuestions(sorted);

        // Inisialisasi default answer untuk A1 (jam kerja) ke 8.0 jika ada
        const a1Question = sorted.find(q => q.code === "A1");
        if (a1Question) {
          setAnswers(prev => ({ ...prev, "A1": 8.0 }));
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  const handleAnswer = (code, value) => {
    setAnswers({ ...answers, [code]: value });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      handleSubmit();
    }
  };

  const handlePrev = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/assessments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ answers }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Gagal menyimpan hasil analisis.");
      }

      localStorage.setItem("hasCompletedTest", "true");
      navigate("/dashboard");
    } catch (err) {
      alert("Terjadi kesalahan: " + err.message);
    }
  };

  const renderInput = (question) => {
    const code = question.code;

    // 1. Avg_Working_Hours_Per_Day (A1) menggunakan range slider
    if (code === "A1") {
      const val = answers[code] !== undefined ? answers[code] : 8.0;
      return (
        <div className="flex flex-col gap-4 mb-8">
          <div className="flex justify-between items-center bg-[#f0f9f1] p-4 rounded-xl border border-gray-100">
            <span className="text-sm font-semibold text-[#0C3B2E]">Jam Kerja Rata-Rata:</span>
            <span className="text-xl font-bold text-[#0C3B2E]">{val} Jam / Hari</span>
          </div>
          <input
            type="range"
            min="1"
            max="24"
            step="0.5"
            value={val}
            onChange={(e) => handleAnswer(code, parseFloat(e.target.value))}
            className="w-full h-2.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#6D9773]"
          />
          <div className="flex justify-between text-[11px] text-gray-400 font-semibold px-1">
            <span>1 Jam</span>
            <span>12 Jam</span>
            <span>24 Jam</span>
          </div>
        </div>
      );
    }

    // Tentukan opsi berdasarkan tipe pertanyaan
    let options = [];

    if (code === "A2") {
      options = [
        { label: "🏢 Kantor (WFO)", value: 0 },
        { label: "🏠 Rumah (WFH)", value: 1 },
        { label: "🔀 Hybrid (Campuran)", value: 2 },
      ];
    } else if (code === "A3") {
      options = [
        { label: "❌ Tidak", value: 0 },
        { label: "✅ Ya", value: 1 },
      ];
    } else if (code === "A5") {
      options = [
        { label: "❌ Tidak Seimbang", value: 0 },
        { label: "✅ Ya, Seimbang", value: 1 },
      ];
    } else if (code.startsWith("G")) {
      // CF questions
      options = [
        { label: "Tidak Pernah", value: 1 },
        { label: "Jarang", value: 2 },
        { label: "Kadang-kadang", value: 3 },
        { label: "Sering", value: 4 },
        { label: "Selalu", value: 5 },
      ];
    } else if (code === "A4") {
      options = [
        { label: "1 - Sangat Tertutup", value: 1 },
        { label: "2 - Cukup Tertutup", value: 2 },
        { label: "3 - Netral", value: 3 },
        { label: "4 - Cukup Terbuka", value: 4 },
        { label: "5 - Sangat Mudah Bergaul", value: 5 },
      ];
    } else if (code === "ML1") {
      options = [
        { label: "1 - Sangat Buruk (Insomnia/Sering Terbangun)", value: 1 },
        { label: "2 - Cukup Buruk", value: 2 },
        { label: "3 - Netral (Biasa)", value: 3 },
        { label: "4 - Cukup Baik", value: 4 },
        { label: "5 - Sangat Nyenyak / Cukup Jam Tidur", value: 5 },
      ];
    } else if (code === "ML2") {
      options = [
        { label: "1 - Tidak Pernah", value: 1 },
        { label: "2 - Jarang (1-2x Sebulan)", value: 2 },
        { label: "3 - Kadang-kadang (1-2x Seminggu)", value: 3 },
        { label: "4 - Sering (3-4x Seminggu)", value: 4 },
        { label: "5 - Setiap Hari", value: 5 },
      ];
    } else if (code === "ML3") {
      options = [
        { label: "1 - Sangat Ringan / Nyaman", value: 1 },
        { label: "2 - Cukup Ringan", value: 2 },
        { label: "3 - Sedang / Netral", value: 3 },
        { label: "4 - Cukup Berat", value: 4 },
        { label: "5 - Sangat Berat (Hampir Burnout)", value: 5 },
      ];
    } else if (code === "ML4") {
      options = [
        { label: "1 - Tidak Ada / Micromanagement Buruk", value: 1 },
        { label: "2 - Kurang Mendukung", value: 2 },
        { label: "3 - Netral", value: 3 },
        { label: "4 - Cukup Mendukung", value: 4 },
        { label: "5 - Dukungan Penuh / Suportif", value: 5 },
      ];
    } else if (code === "ML5") {
      options = [
        { label: "1 - Sangat Tidak Puas", value: 1 },
        { label: "2 - Kurang Puas", value: 2 },
        { label: "3 - Netral", value: 3 },
        { label: "4 - Cukup Puas", value: 4 },
        { label: "5 - Sangat Puas & Bahagia", value: 5 },
      ];
    }

    return (
      <div className="flex flex-col gap-3 mb-8">
        {options.map((opt) => (
          <button
            key={opt.value}
            type="button"
            onClick={() => handleAnswer(code, opt.value)}
            className={`p-4 rounded-xl border-2 transition-all text-left font-medium flex justify-between items-center ${
              answers[code] === opt.value
                ? "border-[#6D9773] bg-[#f0f9f1] text-[#0C3B2E]"
                : "border-gray-200 hover:border-[#6D9773] hover:bg-gray-50 text-gray-600"
            }`}
          >
            <span>{opt.label}</span>
            {answers[code] === opt.value && (
              <span className="w-5 h-5 bg-[#6D9773] rounded-full flex items-center justify-center text-white text-xs">✓</span>
            )}
          </button>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col justify-center items-center font-sans bg-slate-50">
        <div className="w-12 h-12 border-4 border-[#6D9773] border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium">Memuat pertanyaan kuesioner...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col justify-center items-center font-sans bg-slate-50 px-4 text-center">
        <p className="text-red-500 font-bold text-lg mb-4">Gagal terhubung ke backend server.</p>
        <p className="text-gray-500 text-sm mb-6 max-w-md">Pastikan server backend Flask Anda sudah dijalankan dengan benar pada http://localhost:5000.</p>
        <button onClick={() => window.location.reload()} className="bg-[#6D9773] text-white px-6 py-2.5 rounded-full font-bold">
          Coba Lagi
        </button>
      </div>
    );
  }

  const currentQ = questions[currentQuestion];
  const isAnswered = answers[currentQ.code] !== undefined;

  return (
    <div className="min-h-screen flex flex-col font-sans bg-pattern-dots bg-slate-50">
      {/* Header */}
      <nav className="fixed top-0 w-full z-50 bg-[#0C3B2E] text-white px-8 py-4 flex justify-between items-center shadow-md">
        <div className="flex items-center gap-3">
          <img
            src={logoAplikasi}
            alt="Logo"
            className="w-10 h-10 object-contain bg-white rounded-full p-1"
          />
          <h1 className="font-bold text-lg tracking-wide hidden md:block">
            Pendeteksi Tingkat Stress
          </h1>
        </div>
        <Link
          to="/"
          className="text-sm hover:text-[#BB8A52] transition-colors font-medium"
        >
          Kembali ke Beranda
        </Link>
      </nav>

      {/* Main Content (Kuesioner Wizard) */}
      <main className="pt-32 pb-16 px-4 flex flex-col justify-center flex-grow items-center">
        {/* Progress Bar Container */}
        <div className="max-w-xl w-full mb-6">
          <div className="flex justify-between items-end mb-2">
            <span className="text-xs font-bold text-[#0C3B2E] uppercase tracking-wider">
              Kategori: {currentQ.category}
            </span>
            <span className="text-xs font-bold text-[#0C3B2E]">
              Pertanyaan {currentQuestion + 1} / {questions.length}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 shadow-sm">
            <div
              className="bg-[#6D9773] h-2.5 rounded-full transition-all duration-500 ease-out"
              style={{
                width: `${((currentQuestion + 1) / questions.length) * 100}%`,
              }}
            ></div>
          </div>

          <p className="text-[10px] text-gray-500 mt-5 italic text-center">
            *Berikan jawaban yang paling jujur sesuai kondisi Anda dalam beberapa minggu terakhir.
          </p>
        </div>
        
        <div className="bg-white p-8 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] max-w-xl w-full border border-gray-150">
          <div className="mb-4 text-xs text-gray-400 font-bold tracking-widest uppercase">
            {currentQ.code.startsWith("G") ? "Bagian 1: Gejala Stres (CF)" : "Bagian 2: Data Aktivitas (ML)"}
          </div>

          <h2 className="text-xl font-bold text-[#0C3B2E] mb-6 leading-relaxed">
            {currentQ.text}
          </h2>

          {/* Render dinamis input berdasarkan kode pertanyaan */}
          {renderInput(currentQ)}

          {/* Tombol Navigasi */}
          <div className="flex gap-4">
            {currentQuestion > 0 && (
              <button
                type="button"
                onClick={handlePrev}
                className="w-1/3 border-2 border-gray-200 text-gray-600 py-3.5 rounded-full font-bold hover:border-gray-400 hover:bg-gray-50 transition-all shadow-sm"
              >
                Sebelumnya
              </button>
            )}
            <button
              type="button"
              onClick={handleNext}
              disabled={!isAnswered}
              className={`py-3.5 rounded-full font-bold transition-all shadow-md flex-grow ${
                currentQuestion > 0 ? "w-2/3" : "w-full"
              } bg-[#6D9773] text-white hover:bg-[#0C3B2E] disabled:bg-gray-300 disabled:cursor-not-allowed`}
            >
              {currentQuestion === questions.length - 1
                ? "Selesai & Analisis"
                : "Selanjutnya"}
            </button>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Assessment;
