-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 27, 2021 at 07:06 PM
-- Server version: 8.0.18
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `braindb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`) VALUES
(1),
(7),
(11),
(12),
(19),
(20);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `category_description` text COLLATE utf8mb4_general_ci,
  `parent_category` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`, `category_description`, `parent_category`) VALUES
(1, 'Education', NULL, NULL),
(3, 'Public', NULL, 1),
(4, 'Private', NULL, 1),
(5, 'Home', NULL, 1),
(6, 'Geography', NULL, NULL),
(7, 'Religion', NULL, NULL),
(8, 'Science', NULL, NULL),
(9, 'Continents', NULL, 6),
(10, 'Catholicism', NULL, 7),
(11, 'Biology', NULL, 8),
(12, 'North America', NULL, 9),
(14, 'Anatomy', NULL, 11),
(15, 'Space', NULL, NULL),
(17, 'Buddhism', NULL, 7),
(18, 'Roman catholic', NULL, 10),
(19, 'Human anatomy', NULL, 11),
(20, 'Art', NULL, NULL),
(21, 'Literature', NULL, 20),
(22, 'Autobiography', NULL, 21),
(23, 'Music', NULL, NULL),
(24, 'Weather', NULL, NULL),
(25, 'Storms', NULL, 24),
(26, 'Hurricane', NULL, 25),
(27, 'Mid-western', NULL, 24),
(28, 'Puzzles', NULL, NULL),
(29, 'Jigsaw', NULL, 28),
(30, 'Large', NULL, 29),
(31, 'Law', NULL, NULL),
(32, 'Cell phones', NULL, NULL),
(33, 'Apple', NULL, 32),
(34, 'Iphone', NULL, 33),
(38, 'Pinelands', NULL, 3);

-- --------------------------------------------------------

--
-- Table structure for table `pending_videos`
--

CREATE TABLE `pending_videos` (
  `video_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pending_videos`
--

INSERT INTO `pending_videos` (`video_id`) VALUES
(84),
(85),
(87);

-- --------------------------------------------------------

--
-- Table structure for table `userinfo`
--

CREATE TABLE `userinfo` (
  `id` int(11) NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `password` varchar(20) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userinfo`
--

INSERT INTO `userinfo` (`id`, `username`, `email`, `date`, `password`) VALUES
(1, 'SDA', 'SDA123@com.com', NULL, 'SDA'),
(7, 'root', 'root@brainfilms.com', '2021-04-02', 'root'),
(11, '123', '123@1.com', '2021-04-06', '123'),
(12, 'patti', 'patti@none.com', '2021-04-21', 'patti'),
(13, 'RegularUser', 'RegularUser@none.com', '2021-04-25', 'ru'),
(17, 'NormalUser', 'nu12@nu.com', '2021-04-25', 'nu12'),
(18, 'NewUser', 'NewUser@none.com', '2021-04-25', '12qw'),
(19, 'AdminDemo', 'admindemo@none.com', '2021-04-25', 'ad12'),
(20, 'demoadmin', 'demoadmin1@1.com', '2021-04-25', 'demoadmin1');

-- --------------------------------------------------------

--
-- Table structure for table `user_liked_videos`
--

CREATE TABLE `user_liked_videos` (
  `video_id` int(11) NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_liked_videos`
--

INSERT INTO `user_liked_videos` (`video_id`, `username`) VALUES
(86, 'NewUser'),
(82, 'NormalUser'),
(1, 'RegularUser'),
(82, 'root'),
(87, 'root'),
(5, 'SDA'),
(69, 'SDA'),
(82, 'SDA');

-- --------------------------------------------------------

--
-- Table structure for table `user_rated_videos`
--

CREATE TABLE `user_rated_videos` (
  `video_id` int(11) NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_rated_videos`
--

INSERT INTO `user_rated_videos` (`video_id`, `username`, `rating`) VALUES
(5, 'SDA', 5),
(69, 'SDA', 6),
(87, 'root', 6);

-- --------------------------------------------------------

--
-- Table structure for table `video`
--

CREATE TABLE `video` (
  `video_id` int(11) NOT NULL,
  `video_url` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `video_title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `date_added` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video`
--

INSERT INTO `video` (`video_id`, `video_url`, `video_title`, `date_added`) VALUES
(1, 'test', 'tets', '2021-03-15'),
(2, 'www.dumb.com', 'Dumb Video Website', '2001-08-06'),
(3, 'www.IEDK.com', 'Its cool', '2003-07-30'),
(5, 'This is so cool', 'more testingk', '2021-03-15'),
(6, 'www.youtube.com', 'Testing videos', '2021-03-15'),
(7, 'Hello Clas', 'Hi', '2021-03-16'),
(8, 'werwerwe', 'werwerwer', '2021-03-18'),
(9, 'https://stackoverflow.com/questions/21069168/why-is-the-text-in-my-title-tag-showing-up-as-plain-text-on-the-page', 'Why is the text in my title tag showing up as plain text on the page?', '2021-03-19'),
(10, 'https://www.w3schools.com/html/html_links.asp', 'HTML Links', '2021-03-19'),
(11, 'https://stackoverflow.com/questions/51372184/ajax-call-to-flask-to-return-mysql-query', 'Ajax call to flask to return mysql query', '2021-03-19'),
(12, 'https://stackoverflow.com/questions/37631388/how-to-get-data-in-flask-from-ajax-post', 'How to GET data in Flask from AJAX post', '2021-03-19'),
(13, 'https://www.youtube.com/watch?v=IZWtHsM3Y5A', 'Submit AJAX Forms with jQuery and Flask', '2021-03-19'),
(14, 'https://stackoverflow.com/questions/5918144/how-can-i-use-json-data-to-populate-the-options-of-a-select-box/5918179', 'How can I use JSON data to populate the options of a select box?', '2021-03-19'),
(15, 'https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH', 'Python Flask Tutorial:', '2021-03-21'),
(16, 'https://github.com/aparna879/Sentiment-Based-Rating-System/blob/master/movie2.sql', 'Sentiment-Based-Rating-System', '2021-03-21'),
(17, 'https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask', 'Where do I get a SECRET_KEY for Flask?', '2021-03-21'),
(18, 'https://dev.to/blankgodd/connecting-to-a-mysql-database-with-sqlalchemy-lmc', 'Connecting to a MySQL database with SQLAlchemy', '2021-03-21'),
(19, 'https://mysql.wisborg.dk/2019/03/03/using-sqlalchemy-with-mysql-8/', 'Using SQLAlchemy with MySQL 8', '2021-03-21'),
(20, 'https://stackoverflow.com/questions/7296846/how-to-implement-one-to-one-one-to-many-and-many-to-many-relationships-while-de', 'How to implement one-to-one, one-to-many and many-to-many relationships while designing tables?', '2021-03-21'),
(21, 'https://stackoverflow.com/questions/27471099/mysql-relational-tables-how-to-create-multiple-relationships', 'MySQL - Relational tables - How to create multiple relationships?', '2021-03-21'),
(22, 'https://megocode3.wordpress.com/2008/01/04/understanding-a-sql-junction-table/', 'Understanding a SQL Junction Table', '2021-03-21'),
(23, 'https://www.jitsejan.com/python-and-javascript-in-flask.html', 'Using Python and Javascript together with Flask', '2021-03-23'),
(24, 'https://exploreflask.com/en/latest/static.html', 'Static files', '2021-03-23'),
(25, 'https://www.youtube.com/watch?v=hdI2bqOjy3c', 'JavaScript Crash Course For Beginners', '2021-03-23'),
(26, 'https://stackoverflow.com/questions/3968135/mysql-alphabetical-order', 'mysql alphabetical order', '2021-03-23'),
(27, 'https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template', 'How can I pass data from Flask to JavaScript in a template?', '2021-03-23'),
(28, 'https://stackoverflow.com/questions/15321431/how-to-pass-a-list-from-python-by-jinja2-to-javascript', 'How to pass a list from Python, by Jinja2 to JavaScript', '2021-03-23'),
(29, 'https://jinja.palletsprojects.com/en/master/templates/#for', 'https://jinja.palletsprojects.com/en/master/templates/#for', '2021-03-27'),
(30, 'https://stackoverflow.com/questions/30785955/rendering-sql-data-on-html-js-with-flask', 'Rendering SQL data on HTML/JS with Flask', '2021-03-27'),
(31, 'https://flask-wtf.readthedocs.io/en/stable/', 'https://flask-wtf.readthedocs.io/en/stable/', '2021-03-27'),
(32, 'https://stackoverflow.com/questions/21958641/reading-from-database-and-passing-to-javascript-in-flask', 'Reading from database and passing to JavaScript in Flask', '2021-03-27'),
(33, 'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xx-some-javascript-magic', 'The Flask Mega-Tutorial Part XX: Some JavaScript Magic', '2021-03-27'),
(34, 'https://stackoverflow.com/questions/21956500/use-jinja2-template-engine-in-external-javascript-file', 'Use Jinja2 template engine in external javascript file', '2021-03-27'),
(35, 'https://stackoverflow.com/questions/51404129/how-to-access-external-javascript-files-through-jinjaflask', 'How to access external javascript files through jinja[Flask]?', '2021-03-27'),
(36, 'https://stackoverflow.com/questions/3412275/loading-external-script-with-jinja2-template-directive', 'Loading external script with jinja2 template directive', '2021-03-27'),
(37, 'https://stackoverflow.com/questions/16351826/link-to-flask-static-files-with-url-for', 'Link to Flask static files with url_for', '2021-03-27'),
(38, 'https://stackoverflow.com/questions/27917471/pass-parameter-with-python-flask-in-external-javascript', 'Pass parameter with Python Flask in external Javascript', '2021-03-27'),
(39, 'https://medium.com/@crawftv/javascript-jinja-flask-b0ebfdb406b3', 'JavaScript, Jinja & Flask', '2021-03-27'),
(40, 'https://www.youtube.com/watch?v=JRCJ6RtE3xU', ' How to Send Emails Using Python - Plain Text, Adding Attachments, HTML Emails, and More', '2021-03-27'),
(41, 'https://www.youtube.com/watch?v=5iWhQWVXosU', 'Python Quick Tip: Hiding Passwords and Secret Keys in Environment Variables (Mac & Linux)', '2021-03-27'),
(42, 'https://www.javaer101.com/en/article/2922777.html', 'Use Jinja2 template engine in external javascript file', '2021-03-27'),
(43, 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules', '2021-03-27'),
(44, 'https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script', '<script>: The Script element', '2021-03-27'),
(45, 'https://stackoverflow.com/questions/50511034/dynamically-update-javascript-variables-using-jinja', 'Dynamically update Javascript variables using Jinja?', '2021-03-27'),
(46, 'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-ajax', 'The Flask Mega-Tutorial Part XIV: Ajax', '2021-03-27'),
(47, 'https://stackoverflow.com/questions/9183788/js-check-existence-of-a-var-that-equals-0', 'JS: check existence of a var that equals 0', '2021-03-28'),
(48, 'https://memorynotfound.com/dynamically-addremove-items-list-javascript/', 'Dynamically Add/Remove Items From List JavaScript', '2021-03-28'),
(49, 'https://stackoverflow.com/questions/3287336/best-way-to-submit-ul-via-post/3287405', 'Best way to submit UL via POST?', '2021-04-03'),
(50, 'asdfasdf', 'test', '2021-04-03'),
(51, 'https://stackoverflow.com/questions/10903497/python-mysqldb-where-sql-like', 'Python MySQLdb WHERE SQL LIKE', '2021-04-03'),
(52, 'https://stackoverflow.com/questions/33403508/sql-join-on-junction-table-with-many-to-many-relation/33403571', 'SQL join on junction table with many to many relation', '2021-04-03'),
(53, 'https://stackoverflow.com/questions/53445145/flask-optional-path-args', 'Flask - Optional path args', '2021-04-03'),
(54, 'http://www.compciv.org/guides/python/how-tos/creating-proper-url-query-strings/', 'Creating URL query strings in Python', '2021-04-04'),
(55, 'https://www.youtube.com/watch?v=PL6wzmKrgRg', 'Flask query strings - Python on the web - Learning Flask Series Pt. 11', '2021-04-04'),
(56, 'https://stackoverflow.com/questions/6011951/how-to-stop-submit-of-all-of-fields-in-a-div-of-a-form', 'How to stop submit of all of fields in a div of a form?', '2021-04-04'),
(57, 'https://stackoverflow.com/questions/48169611/how-to-use-conditional-if-statements-in-jinja-2', 'How to use conditional if statements in Jinja 2?', '2021-04-04'),
(58, 'asd', '*', '2021-04-04'),
(59, 'https://www.youtube.com/watch?v=C7wfkKrxVXY&t=612s', 'wakawaka', '2021-04-13'),
(60, 'asdf', 'asdf', '2021-04-13'),
(61, 'thisisdumb', 'hmmm', '2021-04-13'),
(62, 'www.testingsteve.com', 'Stevequestions', '2021-04-13'),
(63, 'submitnofilter?', 'no filtersubmit', '2021-04-13'),
(64, 'www.nooo.com', 'www.nooo', '2021-04-13'),
(65, '13.com', '1and3', '2021-04-13'),
(66, 'www.catvideo.com', 'CatVideoTest', '2021-04-21'),
(67, 'zambam', 'zizzle', '2015-12-17'),
(69, 'Http://www.testingmultiadd.com', 'Test', '2021-04-23'),
(70, 'Http://www.testiniadd.com', 'Test', '2021-04-23'),
(71, 'Http://www.asdf.com', 'Test', '2021-04-23'),
(72, 'Https://www.hitestmom.com', 'Hi mom', '2021-04-23'),
(73, 'http://www.testingagain.com', 'Testing Again', '2021-04-23'),
(74, 'http://www.74.com', 'Try again should be 74', '2021-04-23'),
(75, 'http://www.suttlecrash.com', 'Spaceshuttlecrash', '2021-04-23'),
(76, 'http://www.shuttlecrash.com', 'Testing', '2021-04-23'),
(77, 'http://www.resetvideo.com', 'New Video Testing REset', '2021-04-23'),
(78, 'http://www.asldkfjasd.com', 'asdf', '2021-04-23'),
(79, 'http://www.com.com', 'HA HAA', '2021-04-23'),
(80, 'http://www.educationtest.com', 'Education Testing', '2021-04-23'),
(81, 'http://www.ptest.com', 'primarytesterz', '2021-04-23'),
(82, 'http://www.dummyapple.com', 'New Iphone Release', '2021-04-23'),
(84, 'http://www.admindashbaordtestfivido.com', 'AdminDashboard Test Video', '2021-04-25'),
(85, 'Http://www.normaluseraddvideo.com', 'New Video Title - Normal User', '2021-04-25'),
(86, 'http://www.newdemovideo.com', 'New Demo Video', '2021-04-25'),
(87, 'http://www.pinelands.com', 'Pinelands', '2021-04-27');

-- --------------------------------------------------------

--
-- Table structure for table `video_category`
--

CREATE TABLE `video_category` (
  `video_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video_category`
--

INSERT INTO `video_category` (`video_id`, `category_id`) VALUES
(67, 1),
(69, 1),
(80, 5),
(73, 11),
(77, 12),
(76, 15),
(70, 19),
(79, 19),
(78, 21),
(85, 22),
(86, 22),
(74, 26),
(71, 29),
(72, 30),
(81, 31),
(84, 32),
(82, 34),
(87, 38);

-- --------------------------------------------------------

--
-- Table structure for table `video_comments`
--

CREATE TABLE `video_comments` (
  `video_id` int(11) NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `timestamp` datetime NOT NULL,
  `comment` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video_comments`
--

INSERT INTO `video_comments` (`video_id`, `username`, `timestamp`, `comment`) VALUES
(82, 'NormalUser', '2021-04-25 16:11:32', 'Normal Video Comment'),
(82, 'SDA', '2021-04-25 16:12:07', 'Admin Comment'),
(86, 'demoadmin', '2021-04-25 20:13:21', 'Hi this is an admin comment'),
(87, 'NormalUser', '2021-04-27 15:02:33', 'Normal comment'),
(87, 'root', '2021-04-27 15:01:30', 'hi class');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `category_name` (`category_name`),
  ADD KEY `parent_category` (`parent_category`);

--
-- Indexes for table `pending_videos`
--
ALTER TABLE `pending_videos`
  ADD PRIMARY KEY (`video_id`);

--
-- Indexes for table `userinfo`
--
ALTER TABLE `userinfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `user_liked_videos`
--
ALTER TABLE `user_liked_videos`
  ADD PRIMARY KEY (`video_id`,`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `user_rated_videos`
--
ALTER TABLE `user_rated_videos`
  ADD PRIMARY KEY (`video_id`,`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `video`
--
ALTER TABLE `video`
  ADD PRIMARY KEY (`video_id`),
  ADD UNIQUE KEY `unique_url` (`video_url`);

--
-- Indexes for table `video_category`
--
ALTER TABLE `video_category`
  ADD PRIMARY KEY (`video_id`,`category_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `video_comments`
--
ALTER TABLE `video_comments`
  ADD PRIMARY KEY (`video_id`,`username`,`timestamp`),
  ADD KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `userinfo`
--
ALTER TABLE `userinfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `video`
--
ALTER TABLE `video`
  MODIFY `video_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`id`) REFERENCES `userinfo` (`id`);

--
-- Constraints for table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`parent_category`) REFERENCES `categories` (`category_id`);

--
-- Constraints for table `pending_videos`
--
ALTER TABLE `pending_videos`
  ADD CONSTRAINT `pending_videos_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`);

--
-- Constraints for table `user_liked_videos`
--
ALTER TABLE `user_liked_videos`
  ADD CONSTRAINT `user_liked_videos_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`),
  ADD CONSTRAINT `user_liked_videos_ibfk_2` FOREIGN KEY (`username`) REFERENCES `userinfo` (`username`);

--
-- Constraints for table `user_rated_videos`
--
ALTER TABLE `user_rated_videos`
  ADD CONSTRAINT `user_rated_videos_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`),
  ADD CONSTRAINT `user_rated_videos_ibfk_2` FOREIGN KEY (`username`) REFERENCES `userinfo` (`username`);

--
-- Constraints for table `video_category`
--
ALTER TABLE `video_category`
  ADD CONSTRAINT `video_category_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`),
  ADD CONSTRAINT `video_category_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);

--
-- Constraints for table `video_comments`
--
ALTER TABLE `video_comments`
  ADD CONSTRAINT `video_comments_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`),
  ADD CONSTRAINT `video_comments_ibfk_2` FOREIGN KEY (`username`) REFERENCES `userinfo` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
