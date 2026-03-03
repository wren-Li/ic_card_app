<template>
	<view class="container">
		<view class="form-item">
			<text class="label">家长IC卡UID（操作人）：</text>
			<input v-model="operatorUid" placeholder="请读卡" disabled class="input" />
			<button type="default" @click="readOperatorNFC" class="btn-small">读卡</button>
		</view>
		<view class="form-item">
			<text class="label">操作对象：</text>
			<button type="default" @click="queryChildren" class="btn-small">查询绑定的子女</button>
			<picker @change="selectTarget" :value="targetIndex" :range="targetList" range-key="username" class="picker">
				<view class="picker-text">{{targetList[targetIndex]?.username || '请选择操作对象'}}</view>
			</picker>
		</view>
		<view class="form-item">
			<text class="label">积分变动：</text>
			<input v-model="changePoints" placeholder="正数加/负数减" type="number" class="input" />
		</view>
		<view class="form-item">
			<text class="label">操作类型：</text>
			<input v-model="operationType" placeholder="如：消费、奖励、兑换" class="input" />
		</view>
		<button type="primary" @click="updatePoints" class="btn-submit">确认操作</button>
	</view>
</template>
<script>
	export default {
		data() {
			return {
				operatorUid: '',
				targetList: [],
				targetIndex: 0,
				changePoints: 0,
				operationType: '消费'
			}
		},
		methods: {
			readOperatorNFC() {
				// #ifdef APP-PLUS
				if (!plus.nfc) {
					uni.showToast({title: '设备不支持NFC', icon: 'none'});
					return;
				}
				plus.nfc.startDiscovery();
				plus.nfc.addEventListener('nfc', (e) => {
					this.operatorUid = e.tag.uid;
					plus.nfc.stopDiscovery();
					uni.showToast({title: '家长读卡成功'});
					this.queryChildren();
				});
				// #endif
				// #ifndef APP-PLUS
				uni.showToast({title: '仅APP端支持NFC读卡', icon: 'none'});
				// #endif
			},
			queryChildren() {
				if (!this.operatorUid) {
					uni.showToast({title: '请先读取家长IC卡', icon: 'none'});
					return;
				}
				uni.request({
					url: 'http://116aj32013lz6.vicp.fun:37660/api/query',
					method: 'POST',
					data: {card_uid: this.operatorUid},
					success: (res) => {
						if (res.data.code === 200) {
							if (res.data.data.user_type !== 'parent') {
								uni.showToast({title: '仅家长账户可操作！', icon: 'none'});
								this.targetList = [];
								return;
							}
							this.targetList = [{
								card_uid: this.operatorUid,
								username: res.data.data.username + '（自己）'
							}];
							uni.request({
								url: 'http://116aj32013lz6.vicp.fun:37660/api/query_children',
								method: 'POST',
								data: {parent_uid: this.operatorUid},
								success: (res2) => {
									if (res2.data.code === 200) {
										this.targetList = this.targetList.concat(res2.data.data);
									}
								}
							});
						}
					}
				});
			},
			selectTarget(e) {
				this.targetIndex = e.detail.value;
			},
			updatePoints() {
				if (!this.operatorUid) {
					uni.showToast({title: '请先读取家长IC卡', icon: 'none'});
					return;
				}
				if (this.targetList.length === 0 || !this.targetList[this.targetIndex]) {
					uni.showToast({title: '请选择操作对象', icon: 'none'});
					return;
				}
				if (this.changePoints === 0) {
					uni.showToast({title: '积分变动值不能为0', icon: 'none'});
					return;
				}
				const targetUid = this.targetList[this.targetIndex].card_uid;
				uni.request({
					url: 'http://116aj32013lz6.vicp.fun:37660/api/update_points',
					method: 'POST',
					data: {
						operator_uid: this.operatorUid,
						target_uid: targetUid,
						change_points: parseInt(this.changePoints),
						operation_type: this.operationType
					},
					success: (res) => {
						uni.showToast({title: res.data.msg, icon: 'none', duration: 2000});
						if (res.data.code === 200) {
							this.changePoints = 0;
							this.operationType = '消费';
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
	.picker { border: 1px solid #eee; border-radius: 8rpx; padding: 15rpx; margin-top: 10rpx; }
	.picker-text { font-size: 28rpx; color: #333; }
	.btn-submit { height: 80rpx; font-size: 32rpx; border-radius: 10rpx; margin-top: 50rpx; }
</style>