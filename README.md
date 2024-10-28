## 魔方AI实践

### 实践背景

> 改善租房用户App客服体验，结合LLM大模型进行客服解答和找房推荐

### 项目依赖软件、工具

> 安装与使用请自行查阅

* [Ollama](https://ollama.com/) LLM快速搭建工具
* [MilvusDb](https://milvus.io/) 高性能矢量数据库
* [Qwen2.5](https://github.com/QwenLM/Qwen2.5) QWen2.5
* [Python](https://www.python.org/) Python 开发语言


### 启动

> 本项目使用Docker构建环境

```
docker compose -f ./docker/docker-compose.yml up -d --build
```