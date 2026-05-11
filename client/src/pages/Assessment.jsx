import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import logoAplikasi from "../assets/logo-capstone.svg";
import { FaEnvelope, FaGithub } from "react-icons/fa"; 

// Mock Data Pertanyaan dummy
const questions = [
  { id: 1, text: "Seberapa sering Anda merasa kelelahan setelah bekerja?" },
  { id: 2, text: "Apakah Anda sulit berkonsentrasi pada tugas akhir-akhir ini?" },
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
      navigate('/dashboard'); 
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
        <Link to="/" className="text-sm hover:text-[#BB8A52] transition-colors font-medium">
          Kembali ke Beranda
        </Link>
      </nav>

      {/* Main Content (Kuesioner) */}
      <main className="pt-32 pb-16 px-4 flex justify-center flex-grow items-center">
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
                    ? 'border-[#6D9773] bg-[#f0f9f1] text-[#0C3B2E]'
                    : 'border-gray-200 hover:border-[#6D9773] text-gray-600'
                }`}
              >
                {score} - {score === 1 ? 'Sangat Tidak Setuju' : score === 5 ? 'Sangat Setuju' : 'Netral'}
              </button>
            ))}
          </div>

          <button
            onClick={handleNext}
            disabled={!answers[currentQuestion]}
            className="w-full bg-[#6D9773] text-white py-4 rounded-full font-bold hover:bg-[#0C3B2E] disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-md"
          >
            {currentQuestion === questions.length - 1 ? "Selesai & Analisis" : "Selanjutnya"}
          </button>
        </div>
      </main>

      {/* Footer  */}
      <footer id="about" className="bg-[#0C3B2E] text-white px-8 py-16 mt-auto">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold mb-8">About Us</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          
            <div>
              <div className="flex items-center gap-3 mb-4">
                <img
                  src={logoAplikasi}
                  alt="Logo Aplikasi"
                  className="w-10 h-10 object-contain bg-white rounded-full p-1"
                />
                <h3 className="font-bold text-lg tracking-wide">
                  Pendeteksi Tingkat Stress
                </h3>
              </div>
              <p className="text-sm text-gray-300 mb-2 flex items-center gap-2">
                <FaEnvelope className="text-lg" />
                <a
                  href="mailto:CC26-PSU196@student.devacademy.id"
                  className="hover:text-[#BB8A52] transition-colors"
                >
                  CC26-PSU196@student.devacademy.id
                </a>
              </p>
              <p className="text-sm text-gray-300 flex items-center gap-2">
                <FaGithub className="text-lg" />
                <a
                  href="https://github.com/Fathurramz/Pemodelan-Sistem-Pakar-Identifikasi-Tingkat-Stres-Karyawan"
                  target="_blank"
                  rel="noreferrer"
                  className="text-[#BB8A52] hover:underline"
                >
                  GitHub Repository 
                </a>
              </p>
            </div>

            <div>
              <h4 className="font-bold mb-3 border-b border-[#6D9773] pb-2">
                Dibangun Oleh: Tim Capstone CC26-PSU196
              </h4>
              <ul className="text-xs text-gray-300 grid grid-cols-1 gap-2">
                <li>• Ahmad Reyhan Maghribi (FS) - CFCC763D6Y1071</li>
                <li>• Fathur Ramantha (FS) - CFCC471D6Y2275</li>
                <li>• Elan Nurhaliza (AI) - CACC161D6X2324</li>
                <li>
                  • Muhammad Khafidz Miftakhurrohman (AI) - CACC763D6Y1366
                </li>
                <li>• Putri Handayani (DS) - CDCC180D6X2407</li>
                <li>• Stephen Lionel Halim (DS) - CDCC180D6Y1940</li>
              </ul>
            </div>
          </div>

          <hr className="border-[#6D9773]" />
          <p className="text-xs mt-4 text-center text-gray-400">
            © 2026 Tim Capstone CC26-PSU196 DBS Foundation. Dibangun dengan
            React,Tailwind CSS & Doa Ibu
          </p>
        </div>
      </footer>
      
    </div>
  );
};

export default Assessment;