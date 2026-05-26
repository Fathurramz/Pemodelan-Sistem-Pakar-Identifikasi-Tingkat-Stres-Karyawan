
CREATE DATABASE IF NOT EXISTS `stress_detection_db`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `stress_detection_db`;

DROP TABLE IF EXISTS `assessments`;
DROP TABLE IF EXISTS `questions`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `questions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(10) NOT NULL UNIQUE,
    `text` TEXT NOT NULL,
    `category` VARCHAR(100) NOT NULL,
    `order_number` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assessments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `score` INT NOT NULL,
    `stress_level` VARCHAR(50) NOT NULL,
    `factors` JSON NOT NULL,
    `recommendations` JSON NOT NULL,
    `answers` JSON NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_assessments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `questions` (`id`, `code`, `text`, `category`, `order_number`) VALUES
(1, 'G1', 'Tugas yang diberikan perusahaan terasa berlebihan', 'Beban dan Tekanan Kerja', 1),
(2, 'G2', 'Tanggung jawab yang diberikan perusahaan sangat memberatkan saya', 'Beban dan Tekanan Kerja', 2),
(3, 'G3', 'Saya sering dikejar waktu (deadline) dalam menyelesaikan pekerjaan', 'Beban dan Tekanan Kerja', 3),
(4, 'G16', 'Saya merasakan tekanan dari tugas yang dibebankan atasan langsung', 'Konflik Peran dan Penugasan', 4),
(5, 'G18', 'Hubungan saya dengan rekan kerja terasa tidak harmonis atau kurang baik', 'Hubungan Interpersonal di Tempat Kerja', 5),
(6, 'G23', 'Saya merasa kurang jelas dengan informasi dari perusahaan mengenai pekerjaan saya', 'Kejelasan Peran dan Informasi Kerja', 6),
(7, 'G26', 'Saya sulit memperoleh informasi yang dibutuhkan untuk menjalankan pekerjaan', 'Kejelasan Peran dan Informasi Kerja', 7),
(8, 'G33', 'Saya merasa tidak punya peranan dalam pengambilan keputusan di tempat kerja', 'Gaya Kepemimpinan dan Penilaian Kinerja', 8),
(9, 'G37', 'Saya merasa peluang untuk mendapat promosi di perusahaan ini sangat kecil', 'Pengembangan Karir dan Kepuasan Kerja', 9),
(10, 'G38', 'Saya mendapat pekerjaan baru yang memerlukan keterampilan berbeda dari sebelumnya tanpa pelatihan', 'Pengembangan Karir dan Kepuasan Kerja', 10),
(11, 'A1', 'Berapa rata-rata jam kerja Anda per hari?', 'Data Umum dan Kondisi Kerja', 11),
(12, 'A2', 'Di mana Anda biasanya bekerja?', 'Data Umum dan Kondisi Kerja', 12),
(13, 'A3', 'Apakah Anda tinggal bersama keluarga?', 'Data Umum dan Kondisi Kerja', 13),
(14, 'A4', 'Seberapa sosial Anda di lingkungan kerja? (bergaul dan berinteraksi)', 'Data Umum dan Kondisi Kerja', 14),
(15, 'A5', 'Apakah Anda merasa keseimbangan antara pekerjaan dan kehidupan pribadi Anda terjaga?', 'Data Umum dan Kondisi Kerja', 15),
(16, 'ML1', 'Bagaimana kebiasaan tidur Anda akhir-akhir ini?', 'Kesehatan dan Gaya Hidup', 16),
(17, 'ML2', 'Seberapa rutin Anda melakukan aktivitas fisik atau olahraga?', 'Kesehatan dan Gaya Hidup', 17),
(18, 'ML3', 'Seberapa besar tekanan pekerjaan yang Anda rasakan secara keseluruhan?', 'Kesehatan dan Gaya Hidup', 18),
(19, 'ML4', 'Seberapa besar dukungan yang Anda rasakan dari atasan/manajer Anda?', 'Kesehatan dan Gaya Hidup', 19),
(20, 'ML5', 'Seberapa puas Anda dengan pekerjaan yang Anda jalani saat ini?', 'Kesehatan dan Gaya Hidup', 20);
