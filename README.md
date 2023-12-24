# CAJ2PDF Web API

## 项目简介

本项目提供了一个基于 Flask 的 Web API，用于将 CAJ 文件转换为 PDF 格式。该服务封装在 Docker 容器中，便于部署和使用。它基于开源项目 [caj2pdf](https://github.com/caj2pdf/caj2pdf)，该项目允许用户将 CAJ 格式文档转换为 PDF。

## 主要功能

- **API 提供 CAJ 到 PDF 的转换**：用户可以上传 CAJ 文件，服务器会处理并提供 PDF 文件的下载链接。
- **容器化部署**：通过 Docker 容器化，简化环境配置和部署过程。
- **支持多文件上传**：允许一次上传多个 CAJ 文件进行转换。

## 本地部署指南

### 构建 Docker 镜像

在项目根目录下运行以下命令以构建 Docker 镜像：

```bash
docker build -t caj2pdf-web .
#构建后在后台以如下方式运行
docker run -d -p 5000:5000 -v E:/Data/caj2pdf:/data caj2pdf_web
```

### 访问应用

在启动容器后，应用将可通过 http://localhost:5000/api/v1 访问。

也可以使用以下方式，直接从命令行调用caj2pdf，

```
# 首先要找到运行的容器id或名称
docker ps

# 2d10为假设的容器id，需要注意，要转换的文件要先复制到挂载的data目录下
docker exec 2d10 /app/caj2pdf/caj2pdf convert /data/uploads/test.caj -o /data/outputs/yourfile.pdf

```

## REST Client 测试文件示例

`request.http`是一个使用 VS Code 的 REST Client 插件测试 API 的示例。确保 REST Client 插件已安装在您的 VS Code 中。这个 request.http 文件包括三个请求：一个简单的 GET 请求来测试服务是否运行，一个 POST 请求来上传 CAJ 文件，以及一个 GET 请求来下载转换后的 PDF 文件。

```http
@baseurl=http://localhost:5000/api/v1

###
GET {{baseurl}}/hello

###
POST {{baseurl}}/upload
Content-Type: multipart/form-data; boundary=boundary123456

--boundary123456
Content-Disposition: form-data; name="file"; filename="test.caj"
Content-Type: application/octet-stream

< E:\Data\test.caj
--boundary123456--


###
GET {{baseurl}}/download/test.pdf

```
## 贡献

我们欢迎并鼓励社区贡献！如果您想为项目做出贡献，请遵循以下步骤：

- Fork 仓库。
- 创建一个新的分支 (git checkout -b feature/YourFeature).
- 提交您的更改 (git commit -am 'Add some feature').
- 推送到分支 (git push origin feature/YourFeature).
- 创建一个新的 Pull Request。

## 许可证

MIT
