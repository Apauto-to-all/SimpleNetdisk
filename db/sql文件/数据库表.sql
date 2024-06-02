--创建域
--用户表相关域
--创建Uname域，varchar类型，长度为20，用户名
create domain UnameDomain varchar(20)
         constraint Uname_not_null not null;
--创建Passwd域，varchar类型，长度为60，密码
create domain PasswdDomain varchar(60)
		constraint Passwd_not_null not null;
--创建Grade域，smallint类型，等级
create domain GradeDomain smallint;
create domain UspaceDomain int
   constraint U_space CHECK (value >= 0)
   DEFAULT 0;
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
create domain FnameDomain varchar(50)
   constraint Fname_not_null not null;
--创建Fctime域，timestamp类型，文件夹创建时间/文件创建时间
create domain FctimeDomain timestamp 
	CONSTRAINT Fctime_constraint CHECK (value IS NOT NULL)
	DEFAULT CURRENT_TIMESTAMP;
--创建if域，boolean类型，文件夹是否被删除/文件是否被删除/文件还是文件夹
create domain ifDomain boolean 
	CONSTRAINT if_constraint CHECK (value IN (TRUE, FALSE))
	DEFAULT FALSE;
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
create domain IPDomain varchar(32) 
constraint IP_not_null not null;


--密匙表相关域
--创建Kid域，varchar类型，长度为1，密匙ID
create domain KidDomain varchar(1) 
	constraint Kid_default default '1';
--创建Key域，varchar类型，长度为64，密匙
create domain KeyDomain varchar(64);

--等级表
create table Grades(
	Grade GradeDomain primary key,--等级
	Mspace CapacityDomain,--最大容量
	Mupfile CapacityDomain,--最大上传文件大小
	Ktime KtimeDomain--回收站保存时间
);

--用户表
create table Users(
	Uname UnameDomain primary key,--用户名
	Passwd PasswdDomain,--密码
	Grade GradeDomain,--等级
	Uspace UspaceDomain,--使用容量
	Nname NnameDomain,--昵称
	Hpath PathDomain,--头像路径
	foreign key (Grade) references Grades(Grade)
);

--注册码表
create table Rcodes(
	Rcode RcodeDomain primary key,--注册码
	Grade GradeDomain,--对应等级
	Times TimesDomain,--使用次数
	foreign key (Grade) references Grades(Grade)
);

--文件夹表
create table Folders(
	Uname UnameDomain,--用户名
	Foid FidDomain,--文件夹id
	Faid FidDomain,--父级文件夹id
	Foname FnameDomain,--文件夹名
	Foctime FctimeDomain,--文件夹创建时间
	Foifdel ifDomain,--文件夹是否被删除
	Relation PathDomain,--当前文件夹隶属：文件夹的层级关系
	Fopasswd FopasswdDomain,--文件夹密码
	primary key (Uname, Foid),
	foreign key (Uname) references Users(Uname)
);

--文件表
create table Files(
	Uname UnameDomain,--用户名
	Fid FidDomain,--文件id
    Foid FidDomain,--文件夹id
	Finame FnameDomain,--文件名
	Fictime FctimeDomain,--文件创建时间
	Fifdel ifDomain,--文件是否被删除
	FiKB CapacityDomain,--文件大小
	Fipath PathDomain,--文件路径
	primary key (Uname, Fid),
    foreign key (Uname, Foid) references Folders(Uname, Foid),
    foreign key (Uname) references Users(Uname)
);

--垃圾桶表
create table Trash(
	Uname UnameDomain,--用户名
	Fid FidDomain,--文件id
	ForFi ifDomain,--文件还是文件夹
	Ptime timeDomain,--放入回收站时间
	Fideltime timeDomain,--文件删除时间
	primary key (Uname, Fid),
	foreign key (Uname) references Users(Uname),
	foreign key (Uname, Fid) references Files(Uname, Fid)
);

--缩略图表
create table Shrink(
	Fitype FitypeDomain primary key,--文件类型
	Spath PathDomain --缩略图路径
);

--访问日志表
create table Accesslog(
	IP IPDomain,--IP
	Rheader PathDomain,--请求头
	Failnum TimesDomain,--登入失败次数
	primary key (IP, Rheader)
);

--密匙表
create table Keys(
	Kid KidDomain primary key,--密匙id
	Key KeyDomain,--密匙
	Todate timeDomain--到期时间
);