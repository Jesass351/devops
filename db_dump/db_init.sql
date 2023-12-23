CREATE DATABASE IF NOT EXISTS `devops` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `devops`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `alembic_version` (`version_num`) VALUES
('53c53bb775d3');

CREATE TABLE `competitions` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  `place` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `genders` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL
) ENGINE=InnoDB;
INSERT INTO `genders` (`id`, `title`) VALUES
(1, 'Male'),
(2, 'Female');


CREATE TABLE `horses` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender_id` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `jokey_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `horses_to_competitions` (
  `id` int(11) NOT NULL,
  `horse_id` int(11) NOT NULL,
  `competition_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `jokeys` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `rating` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `owners` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `results` (
  `id` int(11) NOT NULL,
  `horse_id` int(11) NOT NULL,
  `competition_id` int(11) NOT NULL,
  `place` int(11) NOT NULL,
  `time` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `desc` text NOT NULL
) ENGINE=InnoDB;
INSERT INTO `roles` (`id`, `title`, `desc`) VALUES
(1, 'admin', 'admin');

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB;
INSERT INTO `users` (`id`, `login`, `password_hash`, `first_name`, `last_name`, `middle_name`, `role_id`) VALUES
(2, 'admin', 'pbkdf2:sha256:600000$blhjgIpCJgnoohIY$7ae6b83a44b6aa520dedc6dd1c7a109473e15dbac577761456b1fab4fe14bfaf', 'Admin', 'Adminovich', NULL, 1);
-- Индексы таблицы `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

ALTER TABLE `competitions`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `genders`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `horses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_horses_gender_id_genders` (`gender_id`),
  ADD KEY `fk_horses_jokey_id_jokeys` (`jokey_id`),
  ADD KEY `fk_horses_owner_id_owners` (`owner_id`);

ALTER TABLE `horses_to_competitions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_horses_to_competitions_competition_id_competitions` (`competition_id`),
  ADD KEY `fk_horses_to_competitions_horse_id_horses` (`horse_id`);

ALTER TABLE `jokeys`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `owners`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_results_competition_id_competitions` (`competition_id`),
  ADD KEY `fk_results_horse_id_horses` (`horse_id`);

ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_users_login` (`login`),
  ADD KEY `fk_users_role_id_roles` (`role_id`);

ALTER TABLE `competitions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `genders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `horses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `horses_to_competitions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `jokeys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `owners`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `horses`
  ADD CONSTRAINT `fk_horses_gender_id_genders` FOREIGN KEY (`gender_id`) REFERENCES `genders` (`id`),
  ADD CONSTRAINT `fk_horses_jokey_id_jokeys` FOREIGN KEY (`jokey_id`) REFERENCES `jokeys` (`id`),
  ADD CONSTRAINT `fk_horses_owner_id_owners` FOREIGN KEY (`owner_id`) REFERENCES `owners` (`id`);

ALTER TABLE `horses_to_competitions`
  ADD CONSTRAINT `fk_horses_to_competitions_competition_id_competitions` FOREIGN KEY (`competition_id`) REFERENCES `competitions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_horses_to_competitions_horse_id_horses` FOREIGN KEY (`horse_id`) REFERENCES `horses` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `results`
  ADD CONSTRAINT `fk_results_competition_id_competitions` FOREIGN KEY (`competition_id`) REFERENCES `competitions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_results_horse_id_horses` FOREIGN KEY (`horse_id`) REFERENCES `horses` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;
