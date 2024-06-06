-- 用户表
CREATE INDEX idx_users_uname ON Users (Uname);
CREATE INDEX idx_users_grade ON Users (Grade);

-- 等级表
CREATE INDEX idx_grades_grade ON Grades (Grade);

-- 注册码表
CREATE INDEX idx_rcodes_rcode ON Rcodes (Rcode);
CREATE INDEX idx_rcodes_grade ON Rcodes (Grade);

-- 文件夹表
CREATE INDEX idx_folders_uid ON Folders (Uname);
CREATE INDEX idx_folders_foid ON Folders (Foid);
CREATE INDEX idx_folders_faid ON Folders (Faid);
CREATE INDEX idx_folders_relation ON Folders (Relation);

-- 文件表
CREATE INDEX idx_files_uid ON Files (Uname);
CREATE INDEX idx_files_fid ON Files (Fid);
CREATE INDEX idx_files_foid ON Files (Foid);

-- 垃圾桶表
CREATE INDEX idx_trash_uid ON Trash (Uname);
CREATE INDEX idx_trash_fid ON Trash (Fid);

-- 缩略图表
CREATE INDEX idx_shrink_fitype ON Shrink (Fitype);

-- 访问日志表
CREATE INDEX idx_accesslog_ip ON Accesslog (IP);
CREATE INDEX idx_accesslog_rheader ON Accesslog (Rheader);

-- 密匙表
CREATE INDEX idx_keys_kid ON Keys (Kid);
