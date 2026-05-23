
CREATE DATABASE IF NOT EXISTS `stress_detection_db`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `stress_detection_db`;


CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `questions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `text` TEXT NOT NULL,
    `category` ENUM('beban_kerja', 'lingkungan_kerja', 'kesehatan') NOT NULL,
    `order_number` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `assessments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `score` INT NOT NULL,
    `stress_level` ENUM('Rendah', 'Sedang', 'Tinggi') NOT NULL,
    `factors` JSON NOT NULL,
    `recommendations` JSON NOT NULL,
    `answers` JSON NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_assessments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `questions` (`id`, `text`, `category`, `order_number`) VALUES

(1, 'Seberapa sering Anda merasa kewalahan dengan jumlah tugas yang harus diselesaikan?', 'beban_kerja', 1),
(2, 'Apakah deadline pekerjaan Anda terasa terlalu menekan?', 'beban_kerja', 2),
(3, 'Seberapa sering Anda harus bekerja lembur atau membawa pekerjaan ke rumah?', 'beban_kerja', 3),
(4, 'Apakah Anda merasa tanggung jawab pekerjaan melebihi kemampuan Anda?', 'beban_kerja', 4),
(5, 'Seberapa sering Anda merasa tidak punya cukup waktu untuk menyelesaikan pekerjaan?', 'beban_kerja', 5),


(6, 'Apakah Anda merasa hubungan dengan rekan kerja kurang harmonis?', 'lingkungan_kerja', 6),
(7, 'Seberapa sering Anda merasa tidak dihargai atau tidak diakui di tempat kerja?', 'lingkungan_kerja', 7),
(8, 'Apakah komunikasi dengan atasan Anda terasa sulit atau menekan?', 'lingkungan_kerja', 8),
(9, 'Seberapa sering terjadi konflik atau ketegangan di lingkungan kerja Anda?', 'lingkungan_kerja', 9),
(10, 'Apakah Anda merasa tidak memiliki kendali atas keputusan yang memengaruhi pekerjaan Anda?', 'lingkungan_kerja', 10),

(11, 'Seberapa sering Anda mengalami kesulitan tidur atau insomnia karena memikirkan pekerjaan?', 'kesehatan', 11),
(12, 'Apakah Anda sering merasa kelelahan fisik meskipun tidak melakukan aktivitas berat?', 'kesehatan', 12),
(13, 'Seberapa sering Anda melewatkan waktu makan atau makan tidak teratur karena pekerjaan?', 'kesehatan', 13),
(14, 'Apakah Anda merasa sulit berkonsentrasi atau mudah lupa akhir-akhir ini?', 'kesehatan', 14),
(15, 'Seberapa sering Anda merasa cemas atau khawatir berlebihan di luar jam kerja?', 'kesehatan', 15);
