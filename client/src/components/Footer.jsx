import { FaEnvelope, FaGithub } from "react-icons/fa";
import logoAplikasi from "../assets/logo-capstone.svg";

const Footer = () => {
  return (
    <footer id="about" className="bg-[#0C3B2E] text-white px-8 py-16 mt-auto">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-2xl font-bold mb-8">About Us</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <img src={logoAplikasi} alt="Logo" className="w-10 h-10 object-contain bg-white rounded-full p-1" />
              <h3 className="font-bold text-lg tracking-wide">Pendeteksi Tingkat Stress</h3>
            </div>
            <p className="text-sm text-gray-300 mb-2 flex items-center gap-2">
              <FaEnvelope className="text-lg" />
              <a href="mailto:CC26-PSU196@student.devacademy.id" className="hover:text-[#BB8A52] transition-colors">CC26-PSU196@student.devacademy.id</a>
            </p>
            <p className="text-sm text-gray-300 flex items-center gap-2">
              <FaGithub className="text-lg" />
              <a href="https://github.com/Fathurramz/Pemodelan-Sistem-Pakar-Identifikasi-Tingkat-Stres-Karyawan" target="_blank" rel="noreferrer" className="text-[#BB8A52] hover:underline">GitHub Repository</a>
            </p>
          </div>

          <div>
            <h4 className="font-bold mb-3 border-b border-[#6D9773] pb-2">Dibangun Oleh: Tim Capstone CC26-PSU196</h4>
            <ul className="text-xs text-gray-300 grid grid-cols-1 gap-2">
              <li>• Ahmad Reyhan Maghribi (FS)</li>
              <li>• Fathur Ramantha (FS)</li>
              <li>• Elan Nurhaliza (AI)</li>
              <li>• Muhammad Khafidz Miftakhurrohman (AI)</li>
              <li>• Putri Handayani (DS)</li>
              <li>• Stephen Lionel Halim (DS)</li>
            </ul>
          </div>
        </div>
        <hr className="border-[#6D9773]" />
        <p className="text-xs mt-4 text-center text-gray-400">
          © 2026 Tim Capstone CC26-PSU196 DBS Foundation. Dibangun dengan React, Tailwind CSS & Doa Ibu
        </p>
      </div>
    </footer>
  );
};

export default Footer;