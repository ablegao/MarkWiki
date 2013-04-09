#主要完善外围消息结构。

1. 用户基础消息  消息类型编号: 1000~1999

2. 频道交互消息  编号 2000~2999

3. 房间或游戏消息 编号 3000~4999

4. 服务器层面交互信息: 5000+

 
#SVN
Revision: 109
http://192.168.0.50/svn/webgame/server/message/room.proto

#文件:


package message;


//***消息规则***********************************************//
// 消息类名称 分 三部分构成									 
// [作用阐述][2][发送类型]									 
// 举例:Login2S  , 登陆 2 Server .  表示发送到服务器			 
//   作用阐述:Login 登陆									 
//   发送类型:s                                             
// 发送类型分3种 ， 2S 客户端发送到服务器, 2C 服务器发送到客户端.
//		2Bc 最初由客户端发 ，而后服务器处理完毕后，将作为广播
//		发出，提醒用户更改。 
//***消息规则***********************************************//


///// === 用户交互信息 = ======================================

// type 1001 ----- 登录 
message Login2S
{
  required string  name = 1;
  required string  password = 2;
}
//message Login2C // 没有该类，会有表示该类的Message::type，收到表示登录失败



// type 1002 // 登录验证通过
message SceneInfo2C 
{
	required string Token  = 1;
	required uint32  uid= 2;
	required uint32 LastChannelId = 3;
}


//Type:1100 获取指定id 的用户信息请求   
message FetchUserInfo2S{
	required uint32 Fuid = 2;
}


//1101 推送用户信息到客户端  
message PutUserInfo2C{
	required uint32 Fuid=1;
	required string Name=2; //用户名称
	required string Faceurl=3; //用户头像
	optional uint32 Win	= 4; //胜利次数
	optional uint32 Lost	= 5; //失败次数
	
}


//// 频道交互数据信息。========================================= 

//Type:2001 发送频道信息列表到客户端  
message PushChannelList2C{
	
	message Channel {
		required uint32 ChannelId= 1;
		required string Name = 2;
		required uint32 State = 3;
	}
	
	repeated  Channel Channels = 1;
}


//Type:2002 获取房间列表请求
message GetChannelRooms2S{
	required bool ChannelId = 1;
	required bool Get =2 [default = true];  
}

//Type:2003 推送房间信息列表到客户端
message PushChannelRooms2C{
	
	message Room {
		required string Domain = 1;
		required uint32 Port =2;
		required string Name = 3;
		required uint32 State = 4;
		required int32  RoomId = 5;
		required uint32 MaxUser =6;
		required uint32 UserCount =7;
	}
	
	repeated  Room Rooms = 1;
}



// ======= 房间内的基本数据消息======================================================


//Type:3000 创建房间 ,, channel 转发给room ,  3000
message RoomCreate2S{
	required string MUid = 1;		//用户编号房主
	required string RoomName = 	2; //房间名称
	required uint32 MapId =3; 		   //地图标记
	required uint32 MaxUser	  = 4; // 最大用户数
	required bool BossExists = 5 [default = false];
	required bool AutoBalance =6 [default = false];
	
}


//Type:3001 房间反馈信息  3001
message RoomCreate2C{
	required uint32 Code = 1;		//创建代码 200 表示正常
	required bool IsError =2 ;		// 是否出现问题  true /false
	required uint32 RoomId	 = 5;   // 房间id . 
}

// Type:3002 设置房间信息。  当客户端发出时，作为设置信息， 而后作为广播信息发出.
message RoomSettingChange2Bc{
	required uint32 RoomId =1;
	optional uint32 MapId = 2;
	optional uint32 MaxUser = 3;
	optional string RoomName = 4;
	optional bool BossExists = 5 [default = false];
	optional bool AutoBalance =6 [default = false];
}

// Type : 3003 获取指定房间详细信息请求
message RoomGetInfo2S{
	required uint32 RoomId = 1;
}

// Type:3004  推送房间信息到客户端。 
message RoomInfoPut2C{
	required string MUid = 1;		//用户编号房主
	required string RoomName = 	2; //房间名称
	required uint32 MapId =3; 		   //地图标记
	required uint32 MaxUser	  = 4; // 最大用户数
	required bool BossExists = 5 [default = false];
	required bool AutoBalance =6 [default = false];
	message UserInfo{
		required uint32 Uid=1;
		required string Name=2;
		required string Faceurl = 3;
	}
	repeated UserInfo Users = 7;
}



//Type: 3005 发送用户状态修改 编号:103
message RoomChangeUserState2Bc{
	required uint32 Uid = 1;
	required uint32 State = 2; // 1，空闲， 2准备。
}


//Type:3006  , 用户选择座位信息
message RoomSelectSeat2Bc{
	required uint32 Uid=1;
	required uint32 Seat =2; //位置
}


//Type 3007 修改游戏状态信息
message RoomChangeState2Bc{
	required uint32 State =1; //1, 等待， 2 ， 开始(等待3秒)， 3 , 运行中
}




//Type:3100
message GameHeroSelect2S{
	required uint32 HeroId=1;
	
}
//Type: 3101 创建NPC 消息 编号:106
message GameCreateNPC2C {
	required uint32 Type = 1;
	required uint32 NpcId =2;
}



//Type: 3102 npc移动广告 编号:107
message GameNPCMove {
	required uint32 NpcId =1;
	
	message Position {
		required uint32 x=1;
		required uint32 y=2;	
	}	
	repeated Position Pos = 2;
}

///// == Room 频道登记处理 =============================================================================

//Type : 5000 注册Room服务器
message RegistRoomServer2Channel{
	required string Domain = 1; // 服务器域名
	required string Port	 =2; //服务器端口
	required uint32 MaxRoom =3;//最大用户数	
}

//Type : 5001 给RoomServer 一个Token
message PushToken2RoomServer{
	optional string Token =1; 	//string 
	required bool  IsError =2;  // 是否出问题
}
//Type:5002 修改Room 最大房间属性
message ChangeServerMaxRoom2Channel{
	required string  Token =1; //服务器token
	required uint32 MaxRoom =2; //变更后的最大人数
}

