-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 12, 2016 at 04:55 PM
-- Server version: 5.6.31-0ubuntu0.14.04.2
-- PHP Version: 5.5.9-1ubuntu4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mishare`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE IF NOT EXISTS `account` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '账号ID',
  `user_id` int(11) NOT NULL COMMENT '账号拥有者的用户ID',
  `site_id` int(11) NOT NULL COMMENT '账号所在的网站ID',
  `username` varchar(32) NOT NULL COMMENT '账号用户名',
  `password` varchar(32) NOT NULL COMMENT '账号密码',
  `max_concurrency_user` int(11) NOT NULL COMMENT '最大同时共享人数',
  `vip_end_date` date NOT NULL COMMENT '会员到期时间',
  `status` tinyint(4) NOT NULL COMMENT '0: 无效(需重新审核), 1: 有效',
  PRIMARY KEY (`account_id`),
  KEY `user_id` (`user_id`),
  KEY `site_id` (`site_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='账号表' AUTO_INCREMENT=7 ;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_id`, `user_id`, `site_id`, `username`, `password`, `max_concurrency_user`, `vip_end_date`, `status`) VALUES
(1, 1, 1, '13727409227', 'aaaa1111', 5, '2016-09-30', 1),
(2, 2, 1, '13710230105', '03545328', 3, '2016-09-29', 0),
(3, 1, 2, '879866023@qq.com', 'ABcd1234', 5, '2016-11-15', 1),
(4, 5, 2, '13710230105', 'slmy03545328', 5, '2016-09-30', 0),
(5, 4, 3, '754281128', 'CHIchi754281128', 5, '2016-10-28', 1),
(6, 3, 3, '13710230105', 'slmy03545328', 5, '2016-09-30', 0);

-- --------------------------------------------------------

--
-- Table structure for table `site`
--

CREATE TABLE IF NOT EXISTS `site` (
  `site_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '网站ID',
  `site_title` varchar(32) NOT NULL COMMENT '网站标题',
  `site_domain` varchar(32) NOT NULL COMMENT '网站域名',
  `site_icon` varchar(128) NOT NULL COMMENT '网站图标',
  `priority` int(11) NOT NULL COMMENT '优先级，数字越小，优先级越大',
  PRIMARY KEY (`site_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='网站表' AUTO_INCREMENT=4 ;

--
-- Dumping data for table `site`
--

INSERT INTO `site` (`site_id`, `site_title`, `site_domain`, `site_icon`, `priority`) VALUES
(1, '爱奇艺', 'www.iqiyi.com', '/static/image/iqiyi.png', 1),
(2, ' 优酷', 'www.youku.com', '/static/image/youku.png', 2),
(3, ' 腾讯视频', 'v.qq.com', '/static/image/tencent.png', 3);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(32) NOT NULL COMMENT '用户名',
  `password` varchar(32) NOT NULL COMMENT '密码（32位大写MD5）',
  `nickname` varchar(32) NOT NULL COMMENT '昵称',
  `portrait` varchar(128) NOT NULL COMMENT '头像URL地址',
  `contribution_value` int(11) NOT NULL DEFAULT '0' COMMENT '剩余贡献值',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='用户表' AUTO_INCREMENT=6 ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `nickname`, `portrait`, `contribution_value`) VALUES
(1, 'liming', 'BC6A4E700FCA7EB9615D8FA1E111FFDF', '李铭', '/static/image/liming.png', 1000),
(2, 'lushutao', 'ECE0F6D7089C743383A23F3A4857B93B', '陆树涛', '/static/image/lushutao.png', 1000),
(3, 'shiqianru', '6F9241F226B75B90D1CA45013DB25A07', '时倩如', '/static/image/shiqianru.png', 1004),
(4, 'huangying', '90C825D81F3C5C3D698BB3EBF8D4F253', '黄莺', '/static/image/huangying.png', 1004),
(5, 'huangjunwei', '79C9257322FA1AF1BDD257C19261DC1F', '黄俊炜', '/static/image/huangjunwei.png', 1000);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
