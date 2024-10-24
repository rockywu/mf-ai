<template>
  <view class="page">
    <scroll-view class="scroll-view" scroll-y scroll-with-animation :scroll-top="top">
      <view style="padding: 30rpx 30rpx 240rpx;">
        <view class="message" :class="[item.userType]" v-for="(item, index) in list" :key="index">
          <image src="../../static/mf-logo.png" v-if="item.userType === 'friend'" class="avatar" mode="widthFix">
          </image>
          <view class="content" v-if="item.messageType === 'room'">
            <div class="links" v-if="item.content && item.content.length > 0">
              <div>房源推荐：</div>
              <a :href="row.link" v-for="(row, i) in buildRespRoomTypesCard(item.content)" :key="i">{{row.name}}</a>
            </div>
            <div v-else>暂无房源</div>
          </view>
          <view class="content" v-else-if="item.messageType === 'store'">
            <div class="links" v-if="item.content && item.content.length > 0">
              <div>门店推荐：</div>
              <a :href="row.link" v-for="(row, i) in buildRespStoresCard(item.content)" :key="i">{{row.name}}</a>
            </div>
            <div v-else>暂无门店</div>
          </view>
          <text class="content" v-else>
            {{ item.content.trim() }}
          </text>
          <image src="../../static//user-logo.png" v-if="item.userType === 'self'" class="avatar" mode="widthFix">
          </image>
        </view>
      </view>
    </scroll-view>
    <view class="tool">
      <input type="text" placeholder="填写找房需求" v-model="content" class="input" @confirm="send" />
      <!-- <image src="../../static/thumb.png" mode="widthFix" class="thumb" @click="chooseImage"></image> -->
      <image src="../../static/i-send.png" mode="widthFix" class="thumb" @click="send"></image>
    </view>
  </view>
</template>

<script>
import { Storage, request } from '../../utils'

const storage = new Storage('mf-content')
export default {
  data() {
    return {
      loading: false,
      content: '',
      list: [],
      top: 0
    };
  },
  onLoad(options) {
    // uni.setNavigationBarTitle({
    //   title: options.name
    // })
    this._friendAvatar = ''
    this._selfAvatar = ''
    this.list = [
      {
        content: '对方历史回复消息',
        userType: 'friend',
        avatar: this._friendAvatar
      },
      {
        content: '历史消息',
        userType: 'self',
        avatar: this._selfAvatar
      }
    ]
  },
  methods: {
    async reqQuestion(question) {
      this.loading = true;
      try {
        const res = await request({
          url: `http://172.21.49.98:11803/api/recommended?question=${question}`
        })
        this.loading = false;
        if (res.statusCode === 200 && res.data.code === 200) {
          return res.data
        }
        return res;
      } catch (e) {
        this.loading = false;
      }
    },
    send() {
      if (this.loading) return;
      if (!this.content) {
        uni.showToast({ icon: 'none', title: '填写您的找房需求' })
        return
      }
      this.list.push({
        content: this.content,
        userType: 'self',
        avatar: this._selfAvatar
      })
      const messageTypes = {
        t_1: 'room',
        t_2: 'store',
        t_3: 'store',
        t_4: 'room',
        t_5: 'text'
      }
      uni.showLoading({title: '...'});
      this.reqQuestion(this.content).then(res => {
        const messageType = messageTypes[`t_${res.type}`] || 'text';
        const rows = res && res.response && res.response.length > 0 ? res.response : [];
        this.pushMsg({
          messageType: messageType,
          content: messageType === 5 ? res.response : rows,
          userType: 'friend',
          avatar: this._friendAvatar
        })
        uni.hideLoading();
        this.scrollToBottom()
      }).catch((e) => {
        uni.hideLoading();
        this.loading = false;
        this.pushMsg({
          messageType: 5,
          content: '未找到相关信息',
          userType: 'friend',
        })
      })
      this.content = ''
      // 模拟对方回复
      this.scrollToBottom()

    },
    pushMsg(params) {
      this.list.push(params)
    },
    buildStoreLink(storeCode) {
      return `https://m.52mf.com/store/${storeCode}`
    },
    buildRoomTypeLink(roomTypeCode) {
      return `https://m.52mf.com/roomType/${roomTypeCode}`
    },
    buildRespStoresCard(rows) {
      return rows.map(v => {
        return {
          link: this.buildStoreLink(v.entity.store_code),
          name: `${v.entity.store_name}(${v.entity.store_address})`
        }
      })
    },
    buildRespRoomTypesCard(rows) {
      return rows.map(v => {
        return {
          link: this.buildRoomTypeLink(v.entity.room_type_code),
          name: `${v.entity.long_term_type_name || '-'}`
        }
      })
    },
    // chooseImage() {
    //   uni.chooseImage({
    //     // sourceType: 'album',
    //     success: (res) => {
    //       this.list.push({
    //         content: res.tempFilePaths[0],
    //         userType: 'self',
    //         messageType: 'image',
    //         avatar: this._selfAvatar
    //       })
    //       this.scrollToBottom()
    //       // 模拟对方回复
    //       setTimeout(() => {
    //         this.list.push({
    //           content: '风景好漂亮啊~',
    //           userType: 'friend',
    //           avatar: this._friendAvatar
    //         })
    //         this.scrollToBottom()
    //       }, 1500)
    //     }
    //   })
    // },
    scrollToBottom() {
      this.top = this.list.length * 1000
    }
  }
}
</script>

<style lang="less" scoped>
.scroll-view {
  /* #ifdef H5 */
  height: calc(100vh - 44px);
  /* #endif */
  /* #ifndef H5 */
  height: 100vh;
  /* #endif */
  background: #eee;
  box-sizing: border-box;
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 30rpx;

  .avatar {
    width: 80rpx;
    height: 80rpx;
    border-radius: 10rpx;
    margin-right: 30rpx;
  }
  .links {
    display: flex;
    flex-direction: column;
    a {
      color: #8080f3;
      display: block;
    }
  }

  .content {
    min-height: 80rpx;
    max-width: 60vw;
    box-sizing: border-box;
    font-size: 28rpx;
    line-height: 1.3;
    padding: 20rpx;
    border-radius: 10rpx;
    background: #fff;

    image {
      width: 200rpx;
    }
  }

  &.self {
    justify-content: flex-end;

    .avatar {
      margin: 0 0 0 30rpx;
    }

    .content {
      position: relative;

      &::after {
        position: absolute;
        content: '';
        width: 0;
        height: 0;
        border: 16rpx solid transparent;
        border-left: 16rpx solid #fff;
        right: -28rpx;
        top: 24rpx;
      }
    }
  }

  &.friend {
    .content {
      position: relative;

      &::after {
        position: absolute;
        content: '';
        width: 0;
        height: 0;
        border: 16rpx solid transparent;
        border-right: 16rpx solid #fff;
        left: -28rpx;
        top: 24rpx;
      }
    }
  }
}

.tool {
  position: fixed;
  width: 100%;
  min-height: 120rpx;
  left: 0;
  bottom: 0;
  background: #fff;
  display: flex;
  align-items: flex-start;
  box-sizing: border-box;
  padding: 20rpx 24rpx 20rpx 40rpx;
  padding-bottom: calc(20rpx + constant(safe-area-inset-bottom)/2) !important;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom)/2) !important;

  .input {
    background: #eee;
    border-radius: 10rpx;
    height: 70rpx;
    margin-right: 30rpx;
    flex: 1;
    padding: 0 20rpx;
    box-sizing: border-box;
    font-size: 28rpx;
  }

  .thumb {
    width: 64rpx;
  }
}
</style>
