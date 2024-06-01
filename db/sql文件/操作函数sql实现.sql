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
;

