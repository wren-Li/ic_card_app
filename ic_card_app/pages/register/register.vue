<template>
	<view class="container">
		<view class="form-item">
			<text class="label">IC卡UID：</text>
			<input v-model="cardUid" placeholder="请贴近NFC读卡" disabled class="input" />
			<button type="default" @click="readNFC" class="btn-small">读卡</button>
		</view>
		<view class="form-item">
			<text class="label">姓名：</text>
			<input v-model="username" placeholder="请输入姓名" class="input" />
		</view>
		<view class="form-item">
			<text class="label">手机号：</text>
			<input v-model="phone" placeholder="请输入手机号" type="number" class="input" />
		</view>
		<view class="form-item">
			<text class="label">账户类型：</text>
			<radio-group @change="changeType" class="radio-group">
				<label class="radio-item"><radio value="parent" checked /> 家长</label>
				<label class="radio-item"><radio value="child" /> 子女</label>
			</radio-group>
		</view>
		<view class="form-item" v-if="userType === 'child'">
			<text class="label">绑定家长IC卡UID：</text>
			<input v-model="parentUid" placeholder="请输入家长的IC卡UID" class="input" />
		</view>
		<button type="primary" @click="register" class="btn-submit">确认开户</button>
	</view>
</template>
<script>
	export default {
		data() {
			return {
				cardUid: '',
				username: '',
				phone: '',
				userType: 'parent',
				parentUid: ''
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
					uni.showToast({title: '读卡成功：' + this.cardUid});
				});
				// #endif
				// #ifndef APP-PLUS
				uni.showToast({title: '仅APP端支持NFC读卡', icon: 'none'});
				// #endif
			},
			changeType(e) {
				this.userType = e.detail.value;
			},
			register() {
				if (!this.cardUid) {
					uni.showToast({title: '请先读取IC卡UID', icon: 'none'});
					return;
				}
				if (!this.username) {
					uni.showToast({title: '请输入姓名', icon: 'none'});
					return;
				}
				if (!this.phone || this.phone.length !== 11) {
					uni.showToast({title: '请输入正确的手机号', icon: 'none'});
					return;
				}
				if (this.userType === 'child' && !this.parentUid) {
					uni.showToast({title: '子女账户必须绑定家长UID', icon: 'none'});
					return;
				}
				uni.request({
					url: 'http://116aj32013lz6.vicp.fun:37660/api/register',
					method: 'POST',
					data: {
						card_uid: this.cardUid,
						username: this.username,
						phone: this.phone,
						user_type: this.userType,
						parent_uid: this.parentUid
					},
					success: (res) => {
						uni.showToast({title: res.data.msg, icon: 'none', duration: 2000});
						if (res.data.code === 200) {
							this.cardUid = '';
							this.username = '';
							this.phone = '';
							this.parentUid = '';
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
	.radio-group { display: flex; gap: 30rpx; margin-top: 10rpx; }
	.radio-item { font-size: 28rpx; }
	.btn-small { width: 100%; margin-top: 10rpx; }
	.btn-submit { height: 80rpx; font-size: 32rpx; border-radius: 10rpx; margin-top: 50rpx; }
</style>