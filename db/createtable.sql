--创建域
--用户表相关域
--创建Uname域，varchar类型，长度为20，用户名
create domain UnameDomain varchar(20);
--创建PassWd域，varchar类型，长度为60，密码
create domain PasswdDomain varchar(60);
--创建Grade域，smallint类型，等级
create domain GradeDomain smallint;
--创建Uspace域，int类型，使用容量
create domain UspaceDomain int;
--创建Nname域，varchar类型，长度20，昵称
create domain NnameDomain varchar(20);
--创建Hpath域，varchar类型，长度50，头像路径
create domain HpathDomain varchar(50);

--注册码表相关域
--创建Rcode域，varchar类型，长度20，注册码
create domain RcodeDomain varchar(20);
--创建Cgrade域，smallint类型,对应等级
create domain CgradeDomain smallint;
--创建Times域，smallint类型，使用次数
create domain TimesDomain smallint;

--等级表相关域
--创建Grade域，smallint类型，等级
--创建Mspace域，int类型，最大容量
create domain MspaceDomain int;
--创建Mupfile域，int类型，最大上传文件大小
create domain MupfileDomain int;
--创建Ktime域，smallint类型，回收站保存时间
create domain KtimeDomain smallint;

--文件夹表相关域
--创建Uname域，varchar类型，长度为20，用户名
--创建Foid域，varchar类型，长度为36，文件夹id
create domain FoidDomain varchar(36);
--创建Faid域，varchar类型，长度为36，父级文件夹id
create domain FaidDomain varchar(36);
--创建FoName域，varchar类型，长度为50，文件夹名
create domain FonameDomain varchar(50);
--创建Foctime域，timestamp类型，文件夹创建时间
create domain FoctimeDomain timestamp;
--创建Foifdel域，boolean类型，文件夹是否被删除
create domain FoifdelDomain boolean;
--创建Relation域，text类型，当前文件夹隶属：文件夹的层级关系
create domain RelationDomain text;
--创建Fopasswd域，varchar类型，长度为60，文件夹密码
create domain FopasswdDomain varchar(60);

--文件表相关域
--创建Uname域，varchar类型，长度为20，用户名
--创建Fid域，varchar类型，长度为20，文件id
create domain FidDomain varchar(20);
--创建Foid域，varchar类型，长度为36，文件夹id，在文件夹表域
--创建FiName域，varchar类型，长度为50，文件名
create domain FinameDomain varchar(50);
--创建FicTime域，timestamp类型，文件创建时间
create domain FictimeDomain timestamp;
--创建Fifdel域，boolean类型，文件是否被删除
create domain FifdelDomain boolean;
--创建FiKB域，int类型，文件大小（KB)
create domain FiKBDomain int;
--创建Fipath域，text类型，文件路径
create domain FipathDomain text;

--垃圾桶表相关域
--创建Uname域，varchar类型，长度为20，用户名
--创建Fid域，varchar类型，长度为36，文件夹id
--创建ForFi域，boolean类型，文件夹还是文件
create domain ForfiDomain boolean;
--创建Ptime域，timestamp类型，放入回收站时间
create domain PtimeDomain timestamp;
--创建Fideltime域，timestamp类型，文件删除时间
create domain FideltimeDomain timestamp;

--缩略图表相关域
--创建Fitype域，varchar类型，长度为20，文件类型
create domain FitypeDomain varchar(20);
--创建Spath域，text类型，缩略图路径
create domain SpathDomain text;

--访问日志表相关域
--创建IP域，varchar类型，长度为32
create domain IPDomain varchar(32);
--创建Rheader域，text类型，请求头
create domain RheaderDomain text;
--创建Failnum域，smallint类型，登入失败次数
create domain FailnumDomain smallint;

--密匙表相关域
--创建Kid域，varchar类型，长度为1，密匙ID
create domain KidDomain varchar(1);
--创建Key域，varchar类型，长度为64，密匙
create domain KeyDomain varchar(64);
--创建Todate域，timestamp类型，过期时间
create domain TodateDomain timestamp;

--建立Grades表，等级表
create table Grades(
	Grade GradeDomain primary key,
	Mspace MspaceDomain,
	Mupfile MupfileDomain,
	Ktime KtimeDomain
);

--创建Users表，用户表
create table Users(
	Uname UnameDomain primary key,
	Passwd PasswdDomain,
	Grade GradeDomain,
	Uspace UspaceDomain default 0,
	Nname NnameDomain,
	Hpath HpathDomain,
	foreign key (Grade) references Grades(Grade)
);

--建立Rcodes表，注册码表
create table Rcodes(
	Rcode RcodeDomain primary key,
	Cgrade CgradeDomain,
	Times TimesDomain
);

--建立Folders表,文件夹表
create table Folders(
	Uname UnameDomain,
	Foid FoidDomain,
	Faid FaidDomain,
	Foname FonameDomain not null,
	Foctime FoctimeDomain DEFAULT CURRENT_TIMESTAMP,
	Foifdel FoifdelDomain DEFAULT FALSE,
	Relation RelationDomain,
	Fopasswd FopasswdDomain,
	primary key (Uname, Foid),
	foreign key (Uname) references Users(Uname)
);

--建立Files表，文件表
create table Files(
	Uname UnameDomain,
	Fid FidDomain,
    Foid FoidDomain,
	Finame FinameDomain not null,
	Fictime FictimeDomain DEFAULT CURRENT_TIMESTAMP,
	Fifdel FifdelDomain DEFAULT FALSE,
	FiKB FiKBDomain,
	Fipath FipathDomain,
	primary key (Uname, Fid),
    foreign key (Uname, Foid) references Folders(Uname, Foid),
    foreign key (Uname) references Users(Uname)
);

create table Trash(
	Uname UnameDomain,
	Fid FoidDomain,
	ForFi ForfiDomain,
	Ptime PtimeDomain,
	Fideltime FideltimeDomain,
	primary key (Uname, Fid),
	foreign key (Uname) references Users(Uname),
	foreign key (Uname, Fid) references Files(Uname, Fid)
);

create table Shrink(
	Fitype FitypeDomain primary key,
	Spath SpathDomain
);

create table Accesslog(
	IP IPDomain not null,
	Rheader RheaderDomain,
	Failnum FailnumDomain,
	primary key (IP, Rheader)
);

create table Keys(
	Kid KidDomain primary key DEFAULT 1,
	Key KeyDomain,
	Todate TodateDomain
);