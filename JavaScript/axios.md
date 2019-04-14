# Axios
## 1. 从浏览器创建XMLHttpRequests
```
axios.get('/user?ID=12345')
    .then(function (response){
        console.log(response)
    })
    .catch(function (error) {
        console.log(error)
    });
```
同样可以用params的方法
```
axios.get('/user'，{params: {ID: 12345}})
    .then(function (response){
        console.log(response)
    })
    .catch(function (error) {
        console.log(error)
    });
```
同样可以用
```
axios.put   axios.post ……
```
更常用的方法是axios API的形式：
```
axios(config):

axios({
    method: 'post', //  'get' ……
    url: 'www.baidu.com',
    data: {
        firstname: 'john',
        lastname: 'Lee'
    }
})
```

在前后端分离的项目中，经常采用的做法是：（以Vue前端/用户登录请求为例）
1. 用户按下登录按钮->login相应api
2. login相应api -> axios实例 + 基本的url、参数params
3. axios拦截器对request做发送前预配置(往往是配置Token) + 接收数据时的response返回
4. 执行then catch操作

- **用户按下登录按钮->login相应api**
[]!()
```
//  用户登录按钮对应方法 -> 'handleLogin'
<el-input
    :type="pwdType"
    v-model="loginForm.password"
    name="password"
    auto-complete="on"
    placeholder="请输入密码"
    @keyup.enter.native="handleLogin" />

//  处理登录事件 -> 'Login'
handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('Login', this.loginForm).then(() => {
            this.loading = false
            this.$router.push({ path: this.redirect || '/' })
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
```

- **login相应api -> axios实例 + 基本的url、参数params**
```
//  处理登录事件Login调用api -> login
export function login(username, password) {
  const data = {
    username,
    password
  }
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}
```

- **axios拦截器对request做发送前预配置(往往是配置Token) + 接收数据时的response返回**
```
// create an axios instance
const service = axios.create({
  baseURL: process.env.BASE_API, // api 的 base_url
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // Do something before request is sent
    if (store.getters.token) {
      // 让每个请求携带token-- ['X-Token']为自定义key 请根据实际情况自行修改
      config.headers['X-Token'] = getToken()
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => response,
  error => {
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
```

- **执行then catch操作**
 ```
因为拦截器会抢先在then 和 catch之前做一些请求和响应的预处理
actions: {
    // 用户名登录
    Login({ commit }, userInfo) {
      const username = userInfo.username.trim()
      return new Promise((resolve, reject) => {
        login(username, userInfo.password)
            .then(response => {
                const data = response.data
                commit('SET_TOKEN', data.token)
                setToken(data.token)
                resolve()
            })
            .catch(error => {
                reject(error)
            })
        })
    },
 ```