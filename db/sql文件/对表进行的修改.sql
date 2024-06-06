--重新创建垃圾桶表，添加Fsharedid属性
create table Trash(
	Uname UnameDomain,--用户名
	Fshareid FidDomain,--文件id和文件夹id
	ForFi ifDomain,--文件还是文件夹
	Ptime timeDomain,--放入回收站时间
	Fideltime timeDomain,--文件删除时间
	primary key (Uname),
	foreign key (Uname) references Users(Uname)
);

create domain CopytimesDomain smallint
  constraint Copytimes_constraint DEFAULT 0;

ALTER TABLE Files
ADD Copytimes CopytimesDomain;

--垃圾桶表的主码更改
DROP TABLE TRASH;
create table Trash(
	Uname UnameDomain,--用户名
	Fshareid FidDomain,--文件id和文件夹id
	ForFi ifDomain,--文件还是文件夹
	Ptime timeDomain,--放入回收站时间
	Fideltime timeDomain,--文件删除时间
	primary key (Uname,Fshareid,ForFi),
	foreign key (Uname) references Users(Uname)
);

DROP USER simple_cloud_user;

-- 创建用户并将角色授权给用户
CREATE USER simple_cloud_user 
WITH PASSWORD 'BiYCR@@Vbkk32$QnbT*VPR&x$Hiy6N';

GRANT select_update_insert_role TO simple_cloud_user;
GRANT trash_delete_role TO simple_cloud_user;