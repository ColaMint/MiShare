-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016 年 09 月 08 日 16:24
-- 服务器版本: 5.5.22
-- PHP 版本: 5.3.10-1ubuntu3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `mishare`
--
DROP DATABASE `mishare`;
CREATE DATABASE `mishare` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `mishare`;

-- --------------------------------------------------------

--
-- 表的结构 `account`
--

CREATE TABLE IF NOT EXISTS `account` (
  `account` int(11) NOT NULL AUTO_INCREMENT COMMENT '账号ID',
  `user_id` int(11) NOT NULL COMMENT '账号拥有者的用户ID',
  `size_id` int(11) NOT NULL COMMENT '账号所在的网站ID',
  `username` varchar(32) NOT NULL COMMENT '账号用户名',
  `password` varchar(32) NOT NULL COMMENT '账号密码',
  `max_concurrency_user` int(11) NOT NULL COMMENT '最大同时共享人数',
  `contribution_value_per_hour` int(11) NOT NULL COMMENT '每使用一小时消耗的贡献值',
  PRIMARY KEY (`account`),
  KEY `user_id` (`user_id`),
  KEY `site_id` (`size_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `site`
--

CREATE TABLE IF NOT EXISTS `site` (
  `site_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '网站ID',
  `site_title` varchar(32) NOT NULL COMMENT '网站标题',
  `site_url` varchar(32) NOT NULL COMMENT '网站URL',
  `site_icon` varchar(128) NOT NULL COMMENT '网站图标',
  PRIMARY KEY (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='网站表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(32) NOT NULL COMMENT '用户名',
  `password` varchar(32) NOT NULL COMMENT '密码（大写MD5）',
  `portrait` varchar(128) NOT NULL COMMENT '头像URL地址',
  `contribution_value` int(11) NOT NULL DEFAULT '0' COMMENT '剩余贡献值',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表' AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
