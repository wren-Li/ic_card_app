<template>
	<view class="container">
		<view class="form-item">
			<text class="label">IC卡UID：</text>
			<input v-model="cardUid" placeholder="请贴近NFC读卡" disabled class="input" />
			<button type="default" @click="readNFC" class="btn-small">读卡</button>
		</view>
		<button type="primary" @click="queryPoints" class="btn-submit">查询积分</button>
		<view class="result-box" v-if="showResult">
			<view class="result-item">
				<text class="key">姓名：</text>
				<text class="value">{{userInfo.username}}</text>
			</view>
			<view class="result-item">
				<text class="key">账户类型：</text>
				<text class="value">{{userInfo.user_type === 'parent' ? '家长' : '子女'}}</text>
			</view>
			<view class="result-item">
				<text class="key">当前积分：</text>
				<text class="value points">{{userInfo.points}}</text>
			</view>
			<view class="records-title" v-if="userInfo.records.length > 0">最近积分记录</view>
			<view class="record-item" v-for="(item, index) in userInfo.records" :key="index">
				<text class="record-time">{{item.operation_time}}</text>
				<text class="record-type">{{item.operation_type}}</text>
				<text class="record-change" :style="item.change_points > 0 ? 'color: red' : 'color: green'">
					{{item.change_points > 0 ? '+' : ''}}{{item.change_points}}
				</text>
				<text class="record-operator">操作人：{{item.operator_name}}</text>
			</view>
		</view>
	</view>
</template>
<script>
	export default {
		data() {
			return {
				cardUid: '',
				showResult: false,
				userInfo: {}
			}
		},
		methods: {
			readNFC() {
				// #ifdef APP-PLUS
				if (!plus.nfc) {
					uni.showToast({title: '设备不支持NFC', icon: 'none'});
					return;
				}
				plus.nfc.startDiscovery();
				plus.nfc.addEventListener('nfc', (e) => {
					this.cardUid = e.tag.uid;
					plus.nfc.stopDiscovery();
					uni.showToast({title: '读卡成功'});
				});
				// #endif
				// #ifndef APP-PLUS
				uni.showToast({title: '仅APP端支持NFC读卡', icon: 'none'});
				// #endif
			},
			queryPoints() {
				if (!this.cardUid) {
					uni.showToast({title: '请先读取IC卡UID', icon: 'none'});
					return;
				}
				uni.request({
					url: 'http://116aj32013lz6.vicp.fun:37660/api/query',
					method: 'POST',
					data: {card_uid: this.cardUid},
					success: (res) => {
						uni.showToast({title: res.data.msg, icon: 'none'});
						if (res.data.code === 200) {
							this.showResult = true;
							this.userInfo = res.data.data;
						}
					},
					fail: () => {
						uni.showToast({title: '网络错误，请检查后端/花生壳', icon: 'none'});
					}
				});
			}
		}
	}
</script>
<style scoped>
	.container { padding: 20rpx; }
	.form-item { margin-bottom: 30rpx; display: flex; flex-direction: column; gap: 10rpx; }
	.label { font-size: 28rpx; color: #333; }
	.input { border: 1px solid #eee; padding: 15rpx; border-radius: 8rpx; font-size: 28rpx; }
	.btn-small { width: 100%; margin-top: 10rpx; }
	.btn-submit { height: 80rpx; font-size: 32rpx; border-radius: 10rpx; margin-bottom: 30rpx; }
	.result-box { border: 1px solid #eee; border-radius: 10rpx; padding: 20rpx; }
	.result-item { display: flex; justify-content: space-between; padding: 10rpx 0; border-bottom: 1px solid #f5f5f5; }
	.key { font-size: 28rpx; color: #666; }
	.value { font-size: 28rpx; color: #333; }
	.points { font-size: 32rpx; color: #2196F3; font-weight: bold; }
	.records-title { font-size: 30rpx; font-weight: bold; margin: 20rpx 0 10rpx; }
	.record-item { display: flex; flex-direction: column; padding: 10rpx 0; border-bottom: 1px solid #f5f5f5; }
	.record-time { font-size: 24rpx; color: #999; }
	.record-type { font-size: 28rpx; margin: 5rpx 0; }
	.record-change { font-size: 28rpx; font-weight: bold; }
	.record-operator { font-size: 24rpx; color: #666; margin-top: 5rpx; }
</style>