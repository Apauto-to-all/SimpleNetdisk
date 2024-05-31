--创建域
--用户表相关域
--创建Uname域，varchar类型，长度为20，用户名
create domain UnameDomain varchar(20) not null;
--创建Passwd域，varchar类型，长度为60，密码
create domain PasswdDomain varchar(60) not null;
--创建Grade域，smallint类型，等级
create domain GradeDomain smallint;
--创建Uspace域，int类型，使用容量
create domain UspaceDomain int default 0;
--创建Nname域，varchar类型，长度20，昵称
create domain NnameDomain varchar(20);
--创建Path域，text类型，头像路径/文件路径/当前文件夹隶属：文件夹的层级关系/缩略图路径/请求头
create domain PathDomain text;

--注册码表相关域
--创建Rcode域，varchar类型，长度20，注册码
create domain RcodeDomain varchar(20);
--创建Times域，smallint类型，使用次数/访问日志表登入失败次数
create domain TimesDomain smallint;

--等级表相关域
--已创建Grade域，在用户表域相关，smallint类型，等级
--创建Capacity域，int类型，最大上传文件大小/最大容量/文件大小/
create domain CapacityDomain int;
--创建Ktime域，smallint类型，回收站保存时间
create domain KtimeDomain smallint;

--文件夹表相关域
--已创建Uname域，在用户表域，varchar类型，长度为20，用户名
--创建Fid域，varchar类型，长度为36，用于文件(夹)id、父级文件夹id
create domain FidDomain varchar(36);
--创建Fname域，varchar类型，长度为50，文件夹名/文件名
create domain FnameDomain varchar(50) not null;
--创建Fctime域，timestamp类型，文件夹创建时间/文件创建时间
create domain FctimeDomain timestamp DEFAULT CURRENT_TIMESTAMP;
--创建if域，boolean类型，文件夹是否被删除/文件是否被删除/文件还是文件夹
create domain ifDomain boolean DEFAULT FALSE;
--创建Fopasswd域，varchar类型，长度为60，文件夹密码
create domain FopasswdDomain varchar(60);

--垃圾桶表相关域
--创建time域，timestamp类型，放入回收站时间/文件删除时间/密匙表过期时间
create domain timeDomain timestamp;

--缩略图表相关域
--创建Fitype域，varchar类型，长度为20，文件类型
create domain FitypeDomain varchar(20);

--访问日志表相关域
--创建IP域，varchar类型，长度为32
create domain IPDomain varchar(32) not null;


--密匙表相关域
--创建Kid域，varchar类型，长度为1，密匙ID
create domain KidDomain varchar(1) DEFAULT 1;
--创建Key域，varchar类型，长度为64，密匙
create domain KeyDomain varchar(64);

--建立Grades表，等级表
create table Grades(
	Grade GradeDomain primary key,
	Mspace CapacityDomain,
	Mupfile CapacityDomain,
	Ktime KtimeDomain
);

--创建Users表，用户表
create table Users(
	Uname UnameDomain primary key,
	Passwd PasswdDomain,
	Grade GradeDomain,
	Uspace UspaceDomain,
	Nname NnameDomain,
	Hpath PathDomain,
	foreign key (Grade) references Grades(Grade)
);

--建立Rcodes表，注册码表
create table Rcodes(
	Rcode RcodeDomain primary key,
	Cgrade GradeDomain,
	Times TimesDomain
);

--建立Folders表,文件夹表
create table Folders(
	Uname UnameDomain,
	Foid FidDomain,
	Faid FidDomain,
	Foname FnameDomain,
	Foctime FctimeDomain,
	Foifdel ifDomain,
	Relation PathDomain,
	Fopasswd FopasswdDomain,
	primary key (Uname, Foid),
	foreign key (Uname) references Users(Uname)
);

--建立Files表，文件表
create table Files(
	Uname UnameDomain,
	Fid FidDomain,
    Foid FidDomain,
	Finame FnameDomain,
	Fictime FctimeDomain,
	Fifdel ifDomain,
	FiKB CapacityDomain,
	Fipath PathDomain,
	primary key (Uname, Fid),
    foreign key (Uname, Foid) references Folders(Uname, Foid),
    foreign key (Uname) references Users(Uname)
);

create table Trash(
	Uname UnameDomain,
	Fid FidDomain,
	ForFi ifDomain,
	Ptime timeDomain,
	Fideltime timeDomain,
	primary key (Uname, Fid),
	foreign key (Uname) references Users(Uname),
	foreign key (Uname, Fid) references Files(Uname, Fid)
);

create table Shrink(
	Fitype FitypeDomain primary key,
	Spath PathDomain
);

create table Accesslog(
	IP IPDomain,
	Rheader PathDomain,
	Failnum TimesDomain,
	primary key (IP, Rheader)
);

create table Keys(
	Kid KidDomain primary key,
	Key KeyDomain,
	Todate timeDomain
);