-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-11-20 08:01:47
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `mydatabase`
--

-- --------------------------------------------------------

--
-- 資料表結構 `course`
--

CREATE TABLE `course` (
  `Cid` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Department` varchar(255) NOT NULL,
  `Credit` int(11) NOT NULL,
  `Members` int(11) NOT NULL,
  `Capacity` int(11) NOT NULL,
  `Time_id` varchar(11) NOT NULL,
  `Is_required` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `course`
--

INSERT INTO `course` (`Cid`, `Name`, `Department`, `Credit`, `Members`, `Capacity`, `Time_id`, `Is_required`) VALUES
(1000, '程式設計', '資訊工程學系', 2, 1, 60, '00-01', 1),
(1001, '微積分', '資訊工程學系', 3, 1, 60, '02-04', 1),
(1002, '程式設計(II)', '資訊工程學系', 2, 0, 60, '16-17', 1),
(1003, '計算機概論', '資訊工程學系', 2, 0, 60, '19-20', 1),
(1004, '線性代數', '資訊工程學系', 2, 0, 60, '21-22', 1),
(1005, '邏輯設計', '資訊工程學系', 2, 1, 60, '33-34', 1),
(1006, '工程數學', '資訊工程學系', 2, 0, 60, '00-01', 0),
(1007, '使用者經驗設計', '資訊工程學系', 3, 0, 60, '61-63', 0),
(1008, '物件導向設計', '資訊工程學系', 3, 0, 60, '47-49', 0),
(1009, '密碼學', '資訊工程學系', 3, 0, 60, '38-40', 0),
(1010, '電子學', '資訊工程學系', 2, 0, 60, '44-45', 0),
(1011, 'UNIX應用與實務', '資訊工程學系', 2, 0, 60, '42-43', 0);

-- --------------------------------------------------------

--
-- 資料表結構 `enrollment`
--

CREATE TABLE `enrollment` (
  `Sid` varchar(11) NOT NULL,
  `Cid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `enrollment`
--

INSERT INTO `enrollment` (`Sid`, `Cid`) VALUES
('D1234567', 1000),
('D1234567', 1001),
('D1234567', 1005);

-- --------------------------------------------------------

--
-- 資料表結構 `student`
--

CREATE TABLE `student` (
  `Sid` varchar(11) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Department` varchar(255) NOT NULL,
  `Grade` int(11) NOT NULL,
  `Credit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `student`
--

INSERT INTO `student` (`Sid`, `Password`, `Name`, `Department`, `Grade`, `Credit`) VALUES
('D1234567', '1234', '王小明', '資訊工程學系', 1, 7);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`Cid`);

--
-- 資料表索引 `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`Sid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
