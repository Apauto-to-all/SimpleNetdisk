--------用户表--------
--检测
select Uname
from Users
where Uname = $1;

--获取信息
select Passwd
from Users
where Uname = $1;

--附加等级表，获取信息
select Hpath,Nname,Mspace,Mupfile
from Grade
where Uname = $1;

--更新 用户名对应的头像路径，昵称
UPDATE Users
SET Hpath= $2, Nname = $3
WHERE username = $1;

--更新 用户名对应的密码
UPDATE Users
SET Passwd = $2
WHERE username = $1;

--插入 注册码表，等级表
--实现功能：`插入`该用户名和密码，
--等级为注册码对应的等级，
--注册码使用次数-1，其他信息默认
INSERT INTO Users (Uname, Passwd, Grade, Uspace, Nname, Hpath)
VALUES ($1, $2, 
        (SELECT Grade FROM Rcodes WHERE Cgrade = $3), 
        '<默认Uspace>', '<默认Nname>', '<默认Hpath>');
UPDATE Rcodes
SET Times = Times - 1
WHERE Rcode = '<注册码>';

--------访问日志表--------
--`查询`数据库中是否存在该ip和浏览器请求头
SELECT * FROM Accesslog
WHERE IP = $1 AND Rheader = $2;

--`查询`数据库中是否存在该ip（请求头为空）
SELECT * FROM Accesslog
WHERE IP = '特定的IP地址' AND Rheader IS NULL;

--`更新`ip+浏览器请求头对应的登入失败次数为0，如果不存在则`插入`
INSERT INTO Accesslog (IP, Rheader, Failnum)
VALUES ($1, $2, 0)
ON DUPLICATE KEY UPDATE Failnum = 0;

--清空访问日志表的所有数据
DELETE FROM Accesslog;

--------密匙表--------
--`查询`数据库中的密匙对应的过期时间，与当前时间比较
SELECT Kid, Key, Todate,
    CASE 
        WHEN Todate > NOW() THEN '未过期'
        ELSE '已过期'
    END AS Status
FROM Keys
WHERE Key = $1;

--`插入`密匙
INSERT INTO Keys (Kid, Key, Todate) 
VALUES ($1, $2, $3);

--------等级表--------
--`插入`等级和对应的最大容量，最大上传文件大小，回收站保存时间
INSERT INTO Grades (Grade, Mspace, Mupfile, Ktime)
 VALUES ($1, $2, $3, $4);

--------注册码表--------
--`查询`数据库中是否存在该注册码
SELECT * FROM Rcodes
WHERE Rcode = $1;

--`插入`该注册码和对应的等级和使用次数
INSERT INTO Rcodes (Rcode, Cgrade, Times) 
VALUES ($1, $2, $3);

--------文件表--------
--检测文件夹
SELECT Uname 
FROM Files 
WHERE Fid = $1;

--获取文件信息
SELECT Foid 
FROM Files 
WHERE Uname = $1 AND Fid = $2;

SELECT * 
FROM Files 
WHERE Uname = $1 AND Fid = $2;

--删除文件
UPDATE Files 
SET Fifdel = 'true' 
WHERE Uname = $1 AND Fid = $2;

--下载文件
SELECT Fipath 
FROM Files 
WHERE Uname = $1 AND Fid = $2;

--重命名
UPDATE Files 
SET Finame = $3 
WHERE Uname = $1 AND Fid = $2;

--插入文件
INSERT INTO Files (Uname, Fid, Foid, Finame, 
Fictime, Fifdel, FiKB, Fipath) 
VALUES ($1, $2, $3, 
$4, CURRENT_TIMESTAMP, 'false', $5, $6);


--------文件夹表--------
--检测文件夹
SELECT * 
FROM Folders 
WHERE Uname = $1 AND Foid = $2;

--获取文件夹信息
SELECT *
FROM Folders 
WHERE Uname = $1 AND Foid = $2;

SELECT Relation
FROM Folders 
WHERE Uname = '特定用户名';

SELECT Faid 
FROM Folders 
WHERE Uname = '特定用户名';

--删除文件夹
UPDATE Folders 
SET Foifdel = true 
WHERE Uname = $1 AND Foid = $2;

--加密文件夹
UPDATE Folders 
SET Fopasswd = $3 
WHERE Uname = $1 AND Foid = $2;

SELECT Fopasswd 
FROM Folders 
WHERE Uname = $1 AND Foid = $2;

UPDATE Folders 
SET Fopasswd = NULL 
WHERE Uname = $1 AND Foid = $2;

--重命名
UPDATE Folders 
SET Foname = $3 
WHERE Uname = $1 AND Foid = $2;

--插入文件夹
INSERT INTO Folders (Uname, Foid, Foname, Fopasswd, 
Fictime, Foifdel, Faid, Relation) 
VALUES ($1, $2, $3, $4, 
CURRENT_TIMESTAMP, 'false', $5, $6);






