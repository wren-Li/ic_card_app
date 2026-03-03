<template>
	<view class="container">
		<button type="primary" @click="goToRegister">IC卡开户</button>
		<button type="default" @click="goToQuery">积分查询</button>
		<button type="warn" @click="goToUpdate">积分增减</button>
	</view>
</template>
<script>
export default {
	methods: {
		goToRegister() { uni.navigateTo({url: '/pages/register/register'}) },
		goToQuery() { uni.navigateTo({url: '/pages/query/query'}) },
		goToUpdate() { uni.navigateTo({url: '/pages/update/update'}) }
	}
}
</script>
<style scoped>
.container { padding: 20rpx; display: flex; flex-direction: column; gap: 20rpx; }
button { height: 80rpx; font-size: 32rpx; border-radius: 10rpx; }
</style>