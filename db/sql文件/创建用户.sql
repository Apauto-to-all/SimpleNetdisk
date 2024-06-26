-- 创建角色并赋予对应的权限
CREATE ROLE select_update_insert_role;
GRANT SELECT, INSERT, UPDATE 
ON ALL TABLES IN 
SCHEMA public TO select_update_insert_role;

-- 创建用户并将角色授权给用户
CREATE USER simple_cloud_user 
WITH PASSWORD 'BiYCR@@Vbkk32$QnbT*VPR&x$Hiy6N';
GRANT select_update_insert_role TO simple_cloud_user;

-- 创建角色并赋予删除权限
CREATE ROLE trash_delete_role;
GRANT DELETE ON Trash TO trash_delete_role;

-- 将角色授予用户
GRANT trash_delete_role TO simple_cloud_user;
