DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) NOT NULL DEFAULT '',
  `path` text NOT NULL,
  `ua` text NOT NULL,
  `referer` text NOT NULL,
  `datetime` int(11) unsigned NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '0',
  `spider` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '1：百度，2：搜狗，3:360,4：谷歌，0：不是蜘蛛',
  PRIMARY KEY (`id`),
  KEY `s` (`status`) USING HASH,
  KEY `d` (`datetime`) USING HASH,
  KEY `sp` (`spider`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
