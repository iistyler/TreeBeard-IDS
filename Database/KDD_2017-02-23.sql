# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: localhost (MySQL 5.7.17)
# Database: KDD
# Generation Time: 2017-02-23 23:51:21 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table testData
# ------------------------------------------------------------

DROP TABLE IF EXISTS `testData`;

CREATE TABLE `testData` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `duration` int(11) DEFAULT '0',
  `udp` int(11) DEFAULT '0',
  `tcp` int(11) DEFAULT '0',
  `icmp` int(11) DEFAULT '0',
  `pm_dump` int(11) DEFAULT '0',
  `tftp_u` int(11) DEFAULT '0',
  `red_i` int(11) DEFAULT '0',
  `tim_i` int(11) DEFAULT '0',
  `X11` int(11) DEFAULT '0',
  `urh_i` int(11) DEFAULT '0',
  `IRC` int(11) DEFAULT '0',
  `Z39_50` int(11) DEFAULT '0',
  `netstat` int(11) DEFAULT '0',
  `ctf` int(11) DEFAULT '0',
  `name` int(11) DEFAULT '0',
  `kshell` int(11) DEFAULT '0',
  `http_443` int(11) DEFAULT '0',
  `exec` int(11) DEFAULT '0',
  `netbios_dgm` int(11) DEFAULT '0',
  `pop_2` int(11) DEFAULT '0',
  `ldap` int(11) DEFAULT '0',
  `link` int(11) DEFAULT '0',
  `netbios_ns` int(11) DEFAULT '0',
  `efs` int(11) DEFAULT '0',
  `daytime` int(11) DEFAULT '0',
  `login` int(11) DEFAULT '0',
  `hostnames` int(11) DEFAULT '0',
  `nnsp` int(11) DEFAULT '0',
  `ssh` int(11) DEFAULT '0',
  `supdup` int(11) DEFAULT '0',
  `uucp_path` int(11) DEFAULT '0',
  `uucp` int(11) DEFAULT '0',
  `klogin` int(11) DEFAULT '0',
  `vmnet` int(11) DEFAULT '0',
  `bgp` int(11) DEFAULT '0',
  `mtp` int(11) DEFAULT '0',
  `sunrpc` int(11) DEFAULT '0',
  `netbios_ssn` int(11) DEFAULT '0',
  `courier` int(11) DEFAULT '0',
  `nntp` int(11) DEFAULT '0',
  `printer` int(11) DEFAULT '0',
  `sql_net` int(11) DEFAULT '0',
  `whois` int(11) DEFAULT '0',
  `rje` int(11) DEFAULT '0',
  `echo` int(11) DEFAULT '0',
  `shell` int(11) DEFAULT '0',
  `systat` int(11) DEFAULT '0',
  `iso_tsap` int(11) DEFAULT '0',
  `domain` int(11) DEFAULT '0',
  `discard` int(11) DEFAULT '0',
  `gopher` int(11) DEFAULT '0',
  `imap4` int(11) DEFAULT '0',
  `remote_job` int(11) DEFAULT '0',
  `csnet_ns` int(11) DEFAULT '0',
  `time` int(11) DEFAULT '0',
  `pop_3` int(11) DEFAULT '0',
  `auth` int(11) DEFAULT '0',
  `ntp_u` int(11) DEFAULT '0',
  `telnet` int(11) DEFAULT '0',
  `urp_i` int(11) DEFAULT '0',
  `finger` int(11) DEFAULT '0',
  `ftp` int(11) DEFAULT '0',
  `eco_i` int(11) DEFAULT '0',
  `ftp_data` int(11) DEFAULT '0',
  `domain_u` int(11) DEFAULT '0',
  `other` int(11) DEFAULT '0',
  `smtp` int(11) DEFAULT '0',
  `http` int(11) DEFAULT '0',
  `private` int(11) DEFAULT '0',
  `ecr_i` int(11) DEFAULT '0',
  `OTH` int(11) DEFAULT '0',
  `S3` int(11) DEFAULT '0',
  `RSTOS0` int(11) DEFAULT '0',
  `S2` int(11) DEFAULT '0',
  `S1` int(11) DEFAULT '0',
  `SH` int(11) DEFAULT '0',
  `RSTO` int(11) DEFAULT '0',
  `RSTR` int(11) DEFAULT '0',
  `REJ` int(11) DEFAULT '0',
  `S0` int(11) DEFAULT '0',
  `SF` int(11) DEFAULT '0',
  `src_bytes` int(11) DEFAULT NULL,
  `dst_bytes` int(11) DEFAULT NULL,
  `land` int(11) DEFAULT NULL,
  `wrong_fragment` int(11) DEFAULT NULL,
  `urgent` int(11) DEFAULT NULL,
  `hot` int(11) DEFAULT NULL,
  `num_failed_logins` int(11) DEFAULT NULL,
  `logged_in` int(11) DEFAULT NULL,
  `num_compromised` int(11) DEFAULT NULL,
  `root_shell` int(11) DEFAULT NULL,
  `su_attempted` int(11) DEFAULT NULL,
  `num_root` int(11) DEFAULT NULL,
  `num_file_creations` int(11) DEFAULT NULL,
  `num_shells` int(11) DEFAULT NULL,
  `num_access_files` int(11) DEFAULT NULL,
  `num_outbound_cmds` int(11) DEFAULT NULL,
  `is_host_login` int(11) DEFAULT NULL,
  `is_guest_login` int(11) DEFAULT NULL,
  `count` int(11) unsigned DEFAULT NULL,
  `serror_rate` float DEFAULT NULL,
  `rerror_rate` float DEFAULT NULL,
  `same_srv_rate` float DEFAULT NULL,
  `diff_srv_rate` float DEFAULT NULL,
  `srv_count` float DEFAULT NULL,
  `srv_serror_rate` float DEFAULT NULL,
  `srv_rerror_rate` float DEFAULT NULL,
  `srv_diff_host_rate` float DEFAULT NULL,
  `dst_host_count` float DEFAULT NULL,
  `dst_host_srv_count` float DEFAULT NULL,
  `dst_host_same_srv_rate` float DEFAULT NULL,
  `dst_host_diff_srv_rate` float DEFAULT NULL,
  `dst_host_same_src_port_rate` float DEFAULT NULL,
  `dst_host_srv_diff_host_rate` float DEFAULT NULL,
  `dst_host_serror_rate` float DEFAULT NULL,
  `dst_host_srv_serror_rate` float DEFAULT NULL,
  `dst_host_rerror_rate` float DEFAULT NULL,
  `dst_host_srv_rerror_rate` float DEFAULT NULL,
  `connection_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
