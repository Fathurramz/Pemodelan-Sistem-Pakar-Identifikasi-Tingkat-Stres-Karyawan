import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import Footer from "../components/Footer";
import logoAplikasi from "../assets/logo-capstone.svg";
import { FaEnvelope, FaGithub } from "react-icons/fa";

const Assessment = () => {
  const [questions, setQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
  const fetchQuestions = async () => {
    try {

      const response = await fetch("http://localhost:5000/api/questions"); 
      
      if (!response.ok) {
        throw new Error(`Server merespons dengan status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data && data.questions) {
        setQuestions(data.questions);
      } else {
        throw new Error("Format data dari API tidak sesuai (.questions tidak ditemukan)");
      }
      
      setIsLoading(false);
    } catch (err) {
      console.error("Error fetching data:", err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  fetchQuestions();
}, []);

  const handleAnswer = (value) => {
    setAnswers({ ...answers, [currentQuestion]: value });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      console.log("Kirim data ke backend:", answers);

      localStorage.setItem("hasCompletedTest", "true");

      navigate("/dashboard");
    }
  };

  // A. Jika data sedang diambil
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center font-sans text-[#0C3B2E] bg-gray-50 font-bold text-lg">
        <div className="text-center">
          <p className="animate-pulse">Memuat pertanyaan dari database...</p>
        </div>
      </div>
    );
  }

  // B. Jika terjadi error koneksi / salah rute API
  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center font-sans bg-gray-50 p-6 text-center">
        <div className="bg-white p-8 rounded-2xl shadow-md border border-red-100 max-w-md">
          <h3 className="text-xl font-bold text-red-600 mb-2">Gagal Memuat Kuesioner</h3>
          <p className="text-gray-600 text-sm mb-6">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-[#6D9773] text-white px-6 py-2 rounded-full font-semibold hover:bg-[#0C3B2E] transition-colors"
          >
            Coba Lagi
          </button>
        </div>
      </div>
    );
  }

  // C. Jika data sukses diambil tapi isinya kosong
  if (!questions || questions.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center font-sans text-gray-600 bg-gray-50">
        Belum ada data pertanyaan di database. Jalankan script seed terlebih dahulu.
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col font-sans bg-pattern-dots">
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

      {/* Main Content (Kuesioner) */}
      <main className="pt-32 pb-16 px-4 flex flex-col justify-center flex-grow items-center">
        {/* Progress Bar Container */}
        <div className="max-w-xl w-full mb-6">
          <div className="flex justify-between items-end mb-2">
            <span className="text-xs font-bold text-[#0C3B2E] uppercase tracking-wider">
              Progress Tes
            </span>
            <span className="text-xs font-bold text-[#0C3B2E]">
              {Math.round(((currentQuestion + 1) / questions.length) * 100)}%
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
            *Berikan jawaban yang paling mendekati perasaan Anda saat ini.
          </p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.08)] max-w-xl w-full border-2 border-gray-100">
          <div className="mb-6 text-sm text-gray-500 font-medium">
            Pertanyaan {currentQuestion + 1} dari {questions.length}
          </div>

          <h2 className="text-xl font-bold text-[#0C3B2E] mb-6 leading-relaxed">
            {questions[currentQuestion].text}
          </h2>

          {/* Opsi Jawaban */}
          <div className="flex flex-col gap-3 mb-8">
            {[1, 2, 3, 4, 5].map((score) => (
              <button
                key={score}
                onClick={() => handleAnswer(score)}
                className={`p-4 rounded-xl border-2 transition-all text-left font-medium ${
                  answers[currentQuestion] === score
                    ? "border-[#6D9773] bg-[#f0f9f1] text-[#0C3B2E]"
                    : "border-gray-200 hover:border-[#6D9773] text-gray-600"
                }`}
              >
                {score} -{" "}
                {score === 1 && "Sangat Tidak Setuju"}
                {score === 2 && "Tidak Setuju"}
                {score === 3 && "Netral"}
                {score === 4 && "Setuju"}
                {score === 5 && "Sangat Setuju"}
              </button>
            ))}
          </div>

          <button
            onClick={handleNext}
            disabled={!answers[currentQuestion]}
            className="w-full bg-[#6D9773] text-white py-4 rounded-full font-bold hover:bg-[#0C3B2E] disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-md"
          >
            {currentQuestion === questions.length - 1
              ? "Selesai & Analisis"
              : "Selanjutnya"}
          </button>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Assessment;
