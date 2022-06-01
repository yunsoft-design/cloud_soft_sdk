# 云软算法 - 访问授权和数据授权

![title](https://raw.githubusercontent.com/yunsoft-design/image/LICENSE/ys_readme_title.png)

## 介绍
云软算法通过访问令牌访问授权,通过明文数据、签名数据、和加密数据对数据授权。</br>
### 安全认证流程
#### 请求方
1 请求方对提交数据（全部或部分）加密。</br>
2 请求方对提交数据（全部或部分）签名。</br>
3 请求方把访问令牌、加密数据、签名数据按每个接口的要求提交到服务端。</br>
#### 服务端
1 验证访问令牌，确保用户身份正确。</br>
2 验证签名，确保请求的确来源于约定的请求方。</br>
3 解密数据，确保数据传输正确完整，未被篡改。</br>

**根据每个接口的安全级别,对全部或部分数据可选择明文、密文、签名**

请扫下面微信公众号【倚云算法】交流,有问必答。</br>

![qrcode](https://raw.githubusercontent.com/yunsoft-design/image/LICENSE/ys_wechat_qrcode.jpg)


