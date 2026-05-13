import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Footer from "../components/Footer";
import logoAplikasi from "../assets/logo-capstone.svg";
import { FaEnvelope, FaGithub } from "react-icons/fa";

// Mock Data Pertanyaan dummy
const questions = [
  { id: 1, text: "Seberapa sering Anda merasa kelelahan setelah bekerja?" },
  {
    id: 2,
    text: "Apakah Anda sulit berkonsentrasi pada tugas akhir-akhir ini?",
  },
  { id: 3, text: "Seberapa sering Anda merasa cemas terkait pekerjaan?" },
];

const Assessment = () => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const navigate = useNavigate();

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
                {score === 1
                  ? "Sangat Tidak Setuju"
                  : score === 5
                    ? "Sangat Setuju"
                    : "Netral"}
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
