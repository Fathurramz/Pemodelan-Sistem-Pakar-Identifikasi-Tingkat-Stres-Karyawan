import { useState } from 'react';
import { Link } from 'react-router-dom';
import Footer from '../components/Footer';
import { FaUserCircle, FaExclamationTriangle, FaCheckCircle, FaEnvelope, FaGithub } from "react-icons/fa";
import logoAplikasi from "../assets/logo-capstone.svg";

const Dashboard = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Mock Data Hasil Analisis
  const userResult = {
    name: "Ahmad Reyhan",
    stressLevel: "Sedang",
    score: 65,
    lastTest: "13 Mei 2026",
    factors: [
      { label: "Beban Kerja", value: 80, color: "bg-red-500" },
      { label: "Lingkungan", value: 45, color: "bg-yellow-500" },
      { label: "Kesehatan", value: 30, color: "bg-green-500" },
    ],
    recommendations: [
      "Ambil jeda istirahat 5-10 menit setiap 2 jam bekerja.",
      "Coba teknik pernapasan kotak (box breathing) saat merasa cemas.",
      "Komunikasikan beban kerja dengan atasan atau rekan tim."
    ]
  };

  return (
    <div className="min-h-screen flex flex-col font-sans bg-slate-50">
      
      {/* Header */}
      <nav className="fixed top-0 w-full z-50 bg-[#0C3B2E] text-white px-8 py-4 flex justify-between items-center shadow-md">
        <div className="flex items-center gap-3">
          <img src={logoAplikasi} alt="Logo" className="w-10 h-10 object-contain bg-white rounded-full p-1" />
          <h1 className="font-bold text-lg tracking-wide hidden md:block">Dashboard Analisis</h1>
        </div>

        {/* Profil & Dropdown */}
        <div className="relative">
          <button 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="flex items-center gap-3 hover:text-[#BB8A52] transition-colors focus:outline-none"
          >
            <span className="text-sm font-medium hidden md:block">Halo, {userResult.name}</span>
            <FaUserCircle className="text-2xl" />
          </button>

          {/* Isi Dropdown */}
          {isDropdownOpen && (
            <div className="absolute right-0 mt-3 w-48 bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden z-50 text-gray-700">
              <Link 
                to="/" 
                className="block px-4 py-3 text-sm hover:bg-gray-50 hover:text-[#0C3B2E] transition-colors border-b border-gray-50"
              >
                Kembali ke Beranda
              </Link>
              <button 
                onClick={() => {
                  alert("Proses Logout...");
                  
                }}
                className="block w-full text-left px-4 py-3 text-sm text-red-600 hover:bg-red-50 hover:font-medium transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>

      <main className="pt-28 pb-16 px-4 md:px-8 max-w-7xl mx-auto w-full flex-grow">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Kolom Kiri Ringkasan Status */}
          <div className="lg:col-span-1 flex flex-col gap-6">
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 text-center">
              <h3 className="text-gray-500 font-medium mb-4">Tingkat Stres Anda</h3>
              <div className="relative inline-flex items-center justify-center mb-4">
                <svg className="w-32 h-32">
                  <circle className="text-gray-200" strokeWidth="10" stroke="currentColor" fill="transparent" r="50" cx="64" cy="64" />
                  <circle className="text-[#BB8A52]" strokeWidth="10" strokeDasharray={314} strokeDashoffset={314 - (314 * userResult.score) / 100} strokeLinecap="round" stroke="currentColor" fill="transparent" r="50" cx="64" cy="64" />
                </svg>
                <span className="absolute text-2xl font-bold text-[#0C3B2E]">{userResult.score}%</span>
              </div>
              <p className={`text-xl font-bold uppercase tracking-widest ${userResult.score > 70 ? 'text-red-600' : 'text-[#6D9773]'}`}>
                {userResult.stressLevel}
              </p>
              <p className="text-xs text-gray-400 mt-2 italic">Tes terakhir: {userResult.lastTest}</p>
            </div>

            <Link to="/assessment" className="w-full bg-[#6D9773] text-white py-4 rounded-xl font-bold text-center hover:bg-[#0C3B2E] transition-all shadow-md">
              Mulai Tes Ulang
            </Link>
          </div>

          {/* Kolom Tengah & Kanan Detail & Rekomendasi */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            
            {/* Grafik Pemicu */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="font-bold text-[#0C3B2E] mb-6 flex items-center gap-2">
                <FaExclamationTriangle className="text-yellow-500" /> Analisis Faktor Pemicu
              </h3>
              <div className="space-y-4">
                {userResult.factors.map((factor, idx) => (
                  <div key={idx}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium text-gray-700">{factor.label}</span>
                      <span className="text-gray-500">{factor.value}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-3">
                      <div className={`${factor.color} h-3 rounded-full transition-all duration-1000 ease-out`} style={{ width: `${factor.value}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Rekomendasi Pakar */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="font-bold text-[#0C3B2E] mb-4 flex items-center gap-2">
                <FaCheckCircle className="text-[#6D9773]" /> Rekomendasi Langkah Awal
              </h3>
              <ul className="space-y-3">
                {userResult.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex gap-3 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg border-l-4 border-[#6D9773]">
                    <span className="font-bold text-[#6D9773]">{idx + 1}.</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
            
          </div>
        </div>
      </main>

     <Footer />
    </div>
  );
};

export default Dashboard;