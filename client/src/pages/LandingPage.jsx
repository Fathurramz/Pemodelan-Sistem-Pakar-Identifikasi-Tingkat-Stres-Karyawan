import { Link } from "react-router-dom";
import logoAplikasi from "../assets/logo-capstone.svg";
import { useState, useEffect } from "react";
import Footer from "../components/Footer";
import {
  FaGithub,
  FaEnvelope,
  FaBrain,
  FaRegFileAlt,
  FaChartBar,
} from "react-icons/fa";

const LandingPage = () => {
  const [activeMenu, setActiveMenu] = useState("home");

  useEffect(() => {
    const handleScroll = () => {
      const testCard = document.getElementById("test-card");
      const about = document.getElementById("about");
      const scrollY = window.scrollY;

      //scroll
      if (about && scrollY >= about.offsetTop - 200) {
        setActiveMenu("about");
      } else if (testCard && scrollY >= testCard.offsetTop - 200) {
        setActiveMenu("test");
      } else {
        setActiveMenu("home");
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="min-h-screen flex flex-col font-sans bg-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 bg-[#0C3B2E] text-white px-8 py-4 flex justify-between items-center shadow-md">
        <div className="flex items-center gap-3">
          <img
            src={logoAplikasi}
            alt="Logo Aplikasi"
            className="w-10 h-10 object-contain bg-white rounded-full p-1"
          />
          <h1 className="font-bold text-lg tracking-wide">
            Pendeteksi Tingkat Stress
          </h1>
        </div>
        <ul className="flex gap-8 font-medium text-sm">
          <li>
            <a
              href="#"
              className={
                activeMenu === "home"
                  ? "text-[#BB8A52]"
                  : "hover:text-[#BB8A52] transition-colors"
              }
            >
              Home
            </a>
          </li>
          <li>
            <a
              href="#test-card"
              className={
                activeMenu === "test"
                  ? "text-[#BB8A52]"
                  : "hover:text-[#BB8A52] transition-colors"
              }
            >
              Test
            </a>
          </li>
         
          <li>
            <a
              href="#about"
              className={
                activeMenu === "about"
                  ? "text-[#BB8A52]"
                  : "hover:text-[#BB8A52] transition-colors"
              }
            >
              About Us
            </a>
          </li>
           <li>
            <Link
              to="/dashboard"
              className="hover:text-[#BB8A52] transition-colors"
            >
              Dashboard
            </Link>
          </li>
        </ul>

      </nav>
      {/* Hero Description Section */}
      <section className="bg-[#6D9773] text-center text-white pt-32 pb-20 px-8">
        <div className="max-w-4xl mx-auto pt-10 mb-16">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-6 tracking-tight leading-tight">
            Pahami Pikiranmu,
            <br /> Temukan Ketenanganmu
          </h2>
          <p className="text-xl font-medium max-w-2xl mx-auto leading-relaxed opacity-95">
            Hanya butuh 5 menit untuk mengukur tingkat stres Anda secara
            objektif. Ambil kendali atas kesejahteraan mental Anda hari ini.
          </p>
        </div>

        {/* Card Mengapa Ini Penting */}
        <div className="bg-[#0C3B2E] text-white rounded-3xl p-10 max-w-5xl mx-auto shadow-xl w-[90%] md:w-full mt-16 ">
          <h2 className="text-3xl font-bold mb-10 text-left">
            Mengapa Ini Penting?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            {/* Poin 1 */}
            <div className="flex flex-col items-center text-center">
              <FaBrain className="text-6xl mb-6 text-gray-200 font-light" />
              <p className="text-sm leading-relaxed text-gray-200">
                <span className="font-bold text-white block mb-1">
                  Identifikasi Dini:
                </span>
                Mencegah burnout sebelum terlambat.
              </p>
            </div>

            {/* Poin 2 */}
            <div className="flex flex-col items-center text-center">
              <FaRegFileAlt className="text-6xl mb-6 text-gray-200 font-light" />
              <p className="text-sm leading-relaxed text-gray-200">
                <span className="font-bold text-white block mb-1">
                  Laporan Personal:
                </span>
                Dapatkan analisis mendalam berdasarkan jawaban Anda.
              </p>
            </div>

            {/* Poin 3 */}
            <div className="flex flex-col items-center text-center">
              <FaChartBar className="text-6xl mb-6 text-gray-200 font-light" />
              <p className="text-sm leading-relaxed text-gray-200">
                <span className="font-bold text-white block mb-1">
                  Langkah Selanjutnya:
                </span>
                Rekomendasi praktis berdasarkan tingkat stres Anda (ringan,
                sedang, atau berat).
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content (Card) */}
      <main
        id="test-card"
        className="bg-pattern-dots pt-32 pb-16 px-4 flex justify-center flex-grow"
      >
        <div className="bg-white border-2 border-gray-100 rounded-3xl p-10 max-w-2xl w-full text-center shadow-[0_8px_30px_rgb(0,0,0,0.08)]">
          <div className="inline-block bg-[#6D9773] text-white px-5 py-1.5 rounded-full text-xs font-semibold mb-6">
            Tes Tingkat Stres
          </div>

          <h2 className="text-3xl font-extrabold text-[#0C3B2E] mb-4 tracking-wide">
            UKUR TINGKAT STRES <br /> ANDA
          </h2>

          <p className="text-sm text-gray-600 mb-8 px-6 leading-relaxed">
            Pengukuran ini membantu menganalisis tingkat stres yang dialami
            karyawan dalam pekerjaan mereka. Mengetahui seberapa besar hal ini
            memengaruhi kondisi mental dan rutinitas keseharian Anda sangatlah
            penting.
          </p>

          {/* Alert Box */}
          <div className="bg-red-50 text-red-500 text-xs p-4 rounded-xl mb-8 border border-red-100 font-medium">
            Kuesioner ini menggunakan skala psikologis yang teruji. Pastikan
            Anda mengisi dengan jujur sesuai kondisi sebenarnya untuk hasil yang
            paling akurat.
          </div>

          <Link
            to="/assessment"
            className="inline-block bg-[#6D9773] hover:bg-[#0C3B2E] text-white px-10 py-3 rounded-full font-bold transition-all duration-300 shadow-md hover:shadow-lg"
          >
            MULAI TES
          </Link>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage;
