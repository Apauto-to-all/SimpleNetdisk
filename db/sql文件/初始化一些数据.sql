-- 插入等级表，等级为1，最大容量为100M，最大上传文件大小为10M，回收站保存时间为10天
INSERT INTO Grades (Grade, Mspace, Mupfile, Ktime) 
VALUES (1, 102400, 10240, 10);

-- 插入等级表，等级为0，最大容量为0M，最大上传文件大小为0M，回收站保存时间为1天
INSERT INTO Grades (Grade, Mspace, Mupfile, Ktime)
VALUES (0, 0, 0, 1);

-- 插入注册码，等级为1，使用次数为2
INSERT INTO Rcodes (Rcode, Grade, Times)
VALUES ('123', 1, 2);
