

create table t_user (
    id int primary key auto_increment ,
    tel varchar(11) unique not null comment '账号',
    password varchar(32) not null comment '密码',

    status int comment '状态，1 代表未激活、2 代表激活、 3 代表 拉黑',
    reg_time datetime comment '注册时间'
);

alter table t_user add alipay_user_id varchar(100) comment '支付宝的用户ID';
alter table t_user add qq_user_id varchar(100) comment 'QQ的用户ID';
alter table t_user add wx_user_id varchar(100) comment '微信的用户ID';

create table t_user_info (
    id int primary key auto_increment ,
    email varchar(50) not null ,
    birth date comment '出生日期',
    nickname varchar(100) comment '昵称',
    realname varchar(100) comment '真实姓名',
    sex varchar(1) comment '性别，m代表 男， f 代表女， s 代表 保密',
    photo longblob comment '用户头像',
    user_id int comment '用户ID'
);

-- 积分配置表 (字典表)
create table t_score_conf (
    id int primary key auto_increment ,
    action varchar(100) comment '动作，注册、上传、评论、下载、...',
    score int comment '动作对应赠送的积分数'
);

insert into t_score_conf(action, score) values('用户注册', 20);
insert into t_score_conf(action, score) values('上传资源', 8);
insert into t_score_conf(action, score) values('评论资源', 2);
insert into t_score_conf(action, score) values('发表帖子', 2);



create table t_user_score(
   id int primary key auto_increment ,
   score int comment '积分',
   remark varchar(100) comment '积分来源',
   create_time datetime comment '积分获取时间',
   user_id int comment '用户ID'
);

-- [id， 资源名，资源描述， 资源类型，资源积分， 资源文件类型，资源存储路径， 资源后缀， 上传资源时间， 上传用户ID , 资源的真实类型]
create table t_resource (
    id int primary key auto_increment,
    res_name varchar(100) comment '资源名称',
    res_type varchar(30) comment '资源类型',
    keyword varchar(50) comment '关键字',
    score int comment '资源下载所需要的积分',
    res_desc text comment '资源描述',
    user_id int comment '上传者',
    ext varchar(20) comment '资源后缀名',
    upload_time datetime comment '资源上传时间',
    size int comment '文件大小',
    res_address varchar(200) comment '资源存储的位置',
);
alter table t_resource add content_type varchar(100) comment '资源的媒体类型，用来做下载用的' ;


create table t_resource_download(
    id int primary key auto_increment,
    user_id int comment '下载资源的用户',
    res_id int comment '下载的资源ID',
    download_time datetime comment '资源下载的时间'
);


-- 资源评论表
create table t_resource_comment(
   id int primary key auto_increment ,
   star int comment '星级',
   content text comment '评论的内容',
   comment_time datetime comment '评论的时间',
   user_id int comment '评论的用户',
   res_id int comment '评论的资源'
);

-- 资源星级配置表 (字典表)
create table t_resource_star_conf (
   star int comment '星级',
   comment_num int comment '评论数'
);

insert into t_resource_star_conf (star, comment_num) values(1, 0);
insert into t_resource_star_conf (star, comment_num) values(2, 3);
insert into t_resource_star_conf (star, comment_num) values(3, 6);
insert into t_resource_star_conf (star, comment_num) values(4, 15);
insert into t_resource_star_conf (star, comment_num) values(5, 30);

-- 查询资源星级
delimiter $$
create procedure get_res_star(in v_res_id int, out v_star int)
begin
  -- 查询资源的 5* 评论有多少个
	declare v_s int default 5 ;
	declare comment_num int default 0;
	declare conf_num int default 0 ;
	set v_star = 0 ; -- 设置默认是 0 *
	star_loop: loop
	    -- 判断 如果 循环到 0 ，则退出循环
		if v_s = 0 then
		   LEAVE  star_loop ;
	    end if ;
	  -- 查询 资源评论表中，某个资源的 N* 对应的评论数
	  select count(1) into comment_num from t_resource_comment
	  where res_id = v_res_id and star >= v_s;

      -- 查询 N*要求的达到的最低评论数
	  select f.comment_num into conf_num from t_resource_star_conf f where star = v_s;
	   -- 如果 评论数达到要求、则获取评论星级
	   if comment_num >= conf_num then
			  set v_star = v_s ;
				LEAVE  star_loop;
		 end if ;
	   -- 控制循环
	   set v_s = v_s - 1 ;
  end loop ;
end $$
delimiter ;

-- 查询资源星级
delimiter $$
create procedure get_res_star2(in v_res_id int)
begin
  -- 查询资源的 5* 评论有多少个
	declare v_s int default 5 ;
	declare comment_num int default 0;
	declare conf_num int default 0 ;
	star_loop: loop
	    -- 判断 如果 循环到 0 ，则退出循环
		if v_s = 0 then
		   LEAVE  star_loop ;
	    end if ;
	  -- 查询 资源评论表中，某个资源的 N* 对应的评论数
	  select count(1) into comment_num from t_resource_comment
	  where res_id = v_res_id and star >= v_s;

      -- 查询 N*要求的达到的最低评论数
	  select f.comment_num into conf_num from t_resource_star_conf f where star = v_s;
	   -- 如果 评论数达到要求、则获取评论星级
	   if comment_num >= conf_num then
			  SELECT v_s;
				LEAVE  star_loop;
		 end if ;
	   -- 控制循环
	   set v_s = v_s - 1 ;
  end loop ;
end $$
delimiter ;


-- 用户资源收藏表
create table t_resource_collect(
   id int primary key auto_increment ,
   res_id int comment '收藏的资源ID',
   user_id int comment '收藏的用户ID',
   collect_time datetime comment '收藏时间'
);


-- 用户好友表 （关注）
create table t_user_friend (
   id int primary key auto_increment ,
   user_id int comment '用户ID',
   friend_id int comment '好友ID',
   create_time datetime comment '关注时间'
);


create table t_logger(
    id int primary key auto_increment,
    realname varchar(100) comment '操作的用户',
    func_name varchar(200) comment '操作的视图函数',
    func_param varchar(200) comment '操作的视图函数需要的参数',
    request_url varchar(100) comment '请求的地址',
    exception_code varchar(20) comment '异常的编码',
    exception_msg text comment '异常的错误信息',
    create_time datetime comment '日志产生的时间'
);


-- 超市管理表
create table t_supplier(
    id varchar(20) primary key,
    s_name varchar(100) comment '供用商名称',
    contacts varchar(100) comment '联系人',
    tel varchar(11) unique not null comment '联系电话',
    addr varchar(100) comment '联系地址',
    fax varchar(12) comment '传真 电话格式0373-*******',
    create_time datetime comment '创建时间',
    desc varchar(200) comment '供应商描述',
);

create table t_bill(
    id int primary key auto_increment,
    s_name varchar(100) comment '商品名称',
    unit varchar(20) comment '商品单位',
    num double comment '商品数量',
    price double comment '总金额',
    sup_id varchar(20) comment '供应商id',
    state varchar(10) comment '是否付款',
    create_time datetime comment '创建时间'
);

create table t_user(
    id int primary key auto_increment,
    username varchar(100) comment '用户名称',
    password varchar(32) not null comment '密码',
    sex varchar(4) comment '性别',
    birth date comment '出生日期',
    tel varchar(11) unique not null comment '用户电话',
    addr varchar(100) comment '用户地址',
    type varchar(5) comment '用户类型'
);