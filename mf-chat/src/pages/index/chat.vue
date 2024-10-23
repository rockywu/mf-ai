<template>
	<view class="content" :style="{ height: heightC - 50 + 'px' }">
		<view class="topone">
			<div class="cmp-logo"></div>
			<view class="topcenter" style="margin-left: 20rpx; width: calc(100% - 130rpx - 80rpx);">
				<view class="topcenter" style="color: #FFFFFF;font-size: 28rpx;font-weight: bold;">邀请好友</view>
				<view class="topcenter" style="color: #FFFFFF;font-size: 22rpx;margin-top: 10rpx;">只有和小伙伴开黑才是最快乐的事情
				</view>
			</view>
			<div style="width: 40rpx;height: 40rpx;margin-right: 20rpx;"></div>
		</view>
		<view class="topone">
			<div class="cmp-logo"></div>
			<view class="topcenter" style="margin-left: 20rpx; width: calc(100% - 130rpx - 80rpx);">
				<view class="topcenter" style="color: #FFFFFF;font-size: 28rpx;font-weight: bold;">完善战队主页</view>
				<view class="topcenter" style="color: #FFFFFF;font-size: 22rpx;margin-top: 10rpx;">快来打造属于你和小伙伴们独一无二的战队吧
				</view>
			</view>
			<div style="width: 40rpx;height: 40rpx;margin-right: 20rpx;"></div>
		</view>
		<!-- 聊天 -->
		<view v-for="(item, idx) in chatList" :key="idx" :class="item.isself ? 'chatself' : 'chatother'">
			<div class="user-logo" v-if="item.isself" /> 
			<div class="ai-logo small" v-else></div>
			<view :class="item.isself ? 'chatbgvS' : 'chatbgvO'">{{ item.msg }}</view>
		</view>
		<!-- input -->
		<view class="chatinput">
			<div class="ai-logo small-icon"></div>
			<input class="inputtext" type="text" placeholder="输入要说的内容" />
			<div class="send-logo"></div>
		</view>
	</view>
</template>

<script>
export default {

	data() {
		return {
			heightC: 0,
			chatList: [{
				isself: true,
				msg: '欢迎新朋友啊、欢迎新朋友啊'
			},
			{
				isself: false,
				msg: '谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢、谢谢谢谢呢'
			},
			{
				isself: true,
				msg: '你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥你叫啥'
			},
			{
				isself: false,
				msg: '我叫某某某我叫某某某我叫某某某我叫'
			},
			{
				isself: true,
				msg: '你叫啥'
			},
			{
				isself: false,
				msg: '我叫某某某'
			},
			{
				isself: true,
				msg: '你叫啥'
			},
			{
				isself: false,
				msg: '我叫某某某'
			},
			{
				isself: true,
				msg: '你叫啥'
			},
			{
				isself: false,
				msg: '我叫某某某'
			}
			]
		};
	},
	onLoad() {
		this.heightC = uni.getSystemInfoSync().windowHeight - uni.getSystemInfoSync().statusBarHeight;
		console.log(this.heightC);
	},
	methods: {

	}
}
</script>

<style lang="less">
.cmp-logo {
	width: 90rpx;
	height: 90rpx;
	margin-left: 20rpx;
	border-radius: 90rpx;
	background: url(../../static/mf-logo.png) no-repeat center center;
	background-size: 100% 100%;
}

.ai-logo,
.user-logo {
	width: 80rpx;
	height: 80rpx;
	border-radius: 80rpx;
}

.ai-logo {
	margin-right: 20rpx;
	background: url(../../static/mf-logo.png) no-repeat center center;
	background-size: 100% 100%;
}
.small-icon {
	width: 40rpx;
	height: 40rpx;
	margin: 0rpx 20rpx;
}

.user-logo {
	margin-left: 20rpx;
	background: url(../../static/user-logo.png) no-repeat center center;
	background-size: 100% 100%;
}
.send-logo {
	width: 58rpx;
	height: 58rpx;
	background: url(../../static/i-send.png) no-repeat center center;
	background-size: 100% 100%;
}

.content {
	position: fixed;
	width: 100%;
	background-color: #0F0F27;
	overflow: scroll;

	.topone {
		width: 90%;
		margin-left: 5%;
		height: 128rpx;
		background-color: #292A3F;
		border-radius: 20rpx;
		margin-top: 20rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.chatself {
		display: flex;
		flex-direction: row-reverse;
		// align-items: center;
		// height: 120rpx;
		width: 90%;
		margin-left: 5%;
		// background-color: #007AFF;
		margin-top: 20rpx;
		margin-bottom: 10rpx;
	}

	.chatother {
		display: flex;
		// align-items: center;
		// height: 120rpx;
		width: 90%;
		margin-left: 5%;
		// background-color: #fc02ff;
		margin-top: 20rpx;
		margin-bottom: 10rpx;
	}

	.chatbgvS {
		color: #FFFFFF;
		padding: 20rpx 40rpx;
		max-width: calc(90% - 140rpx);
		background-color: #292A3F;
		font-size: 24rpx;
		border-radius: 500px 500px 5px 500px;

	}

	.chatbgvO {
		color: #FFFFFF;
		padding: 20rpx 40rpx;
		max-width: calc(90% - 140rpx);
		background-color: #292A3F;
		font-size: 24rpx;
		border-radius: 5px 500px 500px 500px;
	}

	.chatinput {
		position: fixed;
		bottom: 0rpx;
		height: 50px;
		width: 100%;
		background-color: #15152D;
		display: flex;
		// justify-content: space-between;
		align-items: center;

		.inputtext {
			width: calc(100% - 80rpx - 50rpx - 38rpx);
			color: #FFFFFF;
			font-size: 28rpx;
		}
	}
}
</style>
