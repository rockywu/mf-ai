module.exports = {
    devServer: {
      proxy: {
        '/api': {
          target: 'http://localhost:11400', // 代理的目标服务器
          changeOrigin: true,            // 是否改变请求头中的 Host
          pathRewrite: { '^/api': '/api' }   // 重写路径，将 /api 去除
        }
      }
    }
  };
  