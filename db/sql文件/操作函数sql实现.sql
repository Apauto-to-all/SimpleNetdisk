------用户表------ 
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

--访问日志表
--`查询`数据库中是否存在该ip和浏览器请求头
