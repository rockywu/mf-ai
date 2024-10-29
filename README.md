## 魔方AI实践

### 实践背景

> 改善租房用户App客服体验，结合LLM大模型进行客服解答和找房推荐

### 项目依赖软件、工具

> 安装与使用请自行查阅

* [Docker](https://www.docker.com/) Docker容器
* [Ollama](https://ollama.com/) LLM快速搭建工具
* [MilvusDb](https://milvus.io/) 高性能矢量数据库
* [Qwen2.5](https://github.com/QwenLM/Qwen2.5) QWen2.5
* [Python](https://www.python.org/) Python 开发语言
* [sentence-transformers](https://sbert.net/) transformers实现
* [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) 句子转换器模型


### 启动

> 本项目使用Docker构建环境，启动命令，请点击此链接[Docker](https://www.docker.com/)下载安装

* 1、仓库下载： `git@github.com:rockywu/mf-ai.git`
* 2、`cd mf-ai`
*  3、启动运行： `make start ` 或者 `docker compose -f ./docker/docker-compose.yml up -d --build`


### 访问服务

* [http://localhost:11080](http://localhost:11080) api访问地址
*  []
