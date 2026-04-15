# 智扫通机器人智能客服

一个基于 `LangChain Agent + Streamlit + Chroma + Ollama` 的垂直领域 AI 应用示例，面向扫地机器人 / 扫拖一体机场景，提供以下两类核心能力：

- 智能客服问答：结合本地大模型和 RAG 知识库，回答产品使用、选购建议、故障排查、维护保养等问题。
- 个性化使用报告：基于外部结构化数据生成用户月度使用情况分析与建议。

当前仓库更接近教学 / 演示项目，已经具备完整的主链路，但仍存在一些 mock 数据和工程化缺口，适合用于学习 Agent、Prompt 编排、RAG 接入和本地模型部署方式。

## 1. 项目结构

```text
.
├─ app.py                     # Streamlit 对话入口
├─ main.py                    # 示例脚本，与主应用无直接关系
├─ agent/
│  ├─ react_agent.py          # Agent 组装入口
│  └─ tools/
│     ├─ agent_tools.py       # 工具定义：RAG、天气、用户信息、外部数据查询
│     └─ middleware.py        # 工具监控、日志、中间件 Prompt 切换
├─ model/
│  └─ factory.py              # Chat Model / Embedding Model 工厂
├─ rag/
│  ├─ rag_service.py          # 检索后总结链路
│  └─ vector_store.py         # 文档加载、切分、向量入库、Retriever
├─ prompts/                   # 系统提示词、RAG 提示词、报告提示词
├─ config/                    # 模型、向量库、提示词、外部数据配置
├─ data/                      # 知识库数据与外部 CSV 数据
├─ utils/                     # 路径、配置、日志、文件读取等工具
├─ chroma_db/                 # Chroma 持久化目录
└─ logs/                      # 运行日志
```

## 2. 功能概览

### 2.1 智能客服问答

主入口是 `app.py`，前端使用 Streamlit 对话式界面，用户输入问题后会创建或复用 `ReactAgent` 实例，并以流式方式展示回答。

Agent 在 [`agent/react_agent.py`](./agent/react_agent.py) 中组装，包含：

- 模型：本地 `Ollama` 聊天模型
- 工具：
  - `rag_summarize`
  - `get_weather`
  - `get_user_location`
  - `get_user_id`
  - `get_current_month`
  - `fetch_external_data`
  - `fill_context_for_report`
- 中间件：
  - `monitor_tool`：监控工具调用
  - `log_before_model`：记录模型调用前日志
  - `report_prompt_switch`：根据上下文动态切换 Prompt

### 2.2 RAG 检索增强

RAG 相关逻辑位于 `rag/` 目录：

- `VectorStoreService`
  - 使用 `Chroma` 作为本地向量数据库
  - 从 `data/` 目录读取 `.txt` 和 `.pdf` 文件
  - 使用 `RecursiveCharacterTextSplitter` 进行文本切分
  - 使用 md5 文件记录已处理文档，避免重复导入
- `RagSummarizeService`
  - 从向量库检索相关文档
  - 将检索结果拼接进 Prompt
  - 调用模型生成简明回答

### 2.3 报告生成

报告生成是一个单独的业务链路：

1. 获取用户 ID
2. 获取当前月份
3. 调用 `fill_context_for_report`
4. 调用 `fetch_external_data`
5. 中间件检测到报告上下文后切换到报告 Prompt
6. 模型基于结构化数据生成 Markdown 报告

这条链路的设计重点是“运行时上下文驱动 Prompt 切换”，不是单纯依赖用户输入文本做分支判断。

## 3. 技术栈

- Python 3.11+
- Streamlit
- LangChain
- LangGraph / LangChain Middleware
- Chroma
- Ollama
- YAML 配置
- Prompt Engineering

## 4. 环境要求

运行前请确认本机具备以下条件：

1. Python `>= 3.11`
2. 已安装并启动 [Ollama](https://ollama.com/)
3. 已拉取配置中使用的模型：

```bash
ollama pull qwen3:4b
ollama pull qwen3-embedding:4b
```

配置文件默认模型定义在：

- `config/rag.yml`

当前默认值为：

```yaml
chat_model_name : qwen3:4b
embedding_model_name : qwen3-embedding:4b
```

## 5. 依赖安装

当前仓库中的 `pyproject.toml` 尚未完整声明项目依赖，因此推荐先使用现有虚拟环境，或手动安装以下依赖：

```bash
pip install streamlit langchain langgraph langchain-core langchain-community langchain-ollama langchain-chroma langchain-text-splitters pypdf pyyaml
```

如果你使用的是 `uv`，也可以按同样的依赖列表补充到项目环境中。

## 6. 启动方式

### 6.1 启动 Web 应用

在项目根目录执行：

```bash
streamlit run app.py
```

启动后可在浏览器中打开 Streamlit 页面，进行对话式测试。

### 6.2 单独测试 Agent

```bash
python agent/react_agent.py
```

该脚本会直接发送一句“给我生成我的使用报告”，用于测试 Agent 主链路。

### 6.3 构建 / 更新知识库

```bash
python rag/vector_store.py
```

该命令会：

- 扫描 `data/` 目录中的 `.txt` / `.pdf`
- 切分文档
- 生成向量并写入 `chroma_db/`
- 将已处理文件的 md5 记录到 `md5.text`

## 7. 配置说明

### 7.1 模型配置

文件：`config/rag.yml`

- `chat_model_name`：聊天模型名称
- `embedding_model_name`：向量模型名称

### 7.2 向量库配置

文件：`config/chroma.yml`

- `collection_name`：Chroma collection 名称
- `persist_directory`：向量库持久化目录
- `k`：检索召回条数
- `data_path`：知识文档目录
- `md5_hex_store`：已处理文件 md5 记录
- `allow_knowledge_file_type`：允许导入的文件类型
- `chunk_size` / `chunk_overlap` / `separators`：文本切分参数

### 7.3 Prompt 配置

文件：`config/prompts.yml`

- `main_prompt_path`：通用客服 Prompt
- `rag_summarize_prompt_path`：RAG 总结 Prompt
- `report_prompt_path`：报告生成 Prompt

### 7.4 外部数据配置

文件：`config/agent.yml`

- `external_data_path`：外部结构化数据 CSV 路径

## 8. 数据说明

### 8.1 知识库数据

`data/` 目录中存放知识库原始资料，包括：

- 产品问答
- 选购指南
- 维护保养
- 故障排除
- PDF / TXT 文档

这些数据会被加载进 Chroma，用于 `rag_summarize` 工具的检索增强问答。

### 8.2 外部结构化数据

`data/external/records.csv` 用于模拟用户月度使用记录，字段包括：

- 用户 ID
- 用户特征
- 清洁效率
- 耗材状态
- 对比信息
- 时间

报告生成功能会读取这份数据，并转成按 `user_id -> month -> record` 的内存结构，再供模型生成报告。

## 9. 核心实现说明

### 9.1 Agent 设计

`agent/react_agent.py` 使用 `create_agent(...)` 创建智能体，将模型、工具、中间件统一拼装，形成一条完整执行链路。

### 9.2 中间件机制

`agent/tools/middleware.py` 负责三类横切逻辑：

- 工具调用日志记录
- 模型调用前日志记录
- 报告场景 Prompt 动态切换

其中 `fill_context_for_report` 本身不负责业务查询，而是通过中间件把 `runtime.context["report"]` 标记为 `True`，从而触发报告 Prompt 切换。这是项目里比较关键的设计点。

### 9.3 流式输出

`app.py` 中通过 `write_stream(...)` 将 Agent 的流式输出逐字符展示到页面上，形成对话式交互体验。

## 10. 当前已知限制

这部分很重要，接手前建议先了解：

1. 天气、用户位置、用户 ID、当前月份等工具当前是 mock 数据，返回值来自固定文本或随机选择，不是真实业务系统接入。
2. `pyproject.toml` 还没有补齐实际依赖，环境复现能力有限。
3. 向量库去重依赖 `md5.text`，只避免重复导入，不会清理“已修改文件”的旧向量数据。
4. 仓库中包含 `.venv/`、`logs/`、`chroma_db/` 等运行产物，更适合本地演示，不适合作为干净的发布仓库。
5. 项目尚未包含自动化测试、README 之外的部署说明和 CI 配置。
6. 外部 CSV 使用手工解析方式读取，适合演示，不适合复杂生产数据场景。

## 11. 后续优化建议

如果准备继续演进，建议优先做以下改造：

1. 补齐 `pyproject.toml` 依赖声明，统一环境安装方式。
2. 将 mock 工具替换为真实接口或可配置数据源。
3. 为知识库构建增加“全量重建 / 增量更新 / 删除旧索引”能力。
4. 增加基础单元测试和集成测试。
5. 清理仓库中的本地运行产物，并补充 `.gitignore`。
6. 将报告数据读取逻辑替换为更稳健的 CSV / 数据库访问实现。

## 12. 快速体验建议

首次运行推荐按下面顺序操作：

1. 启动 Ollama，并确认模型已拉取完成
2. 执行 `python rag/vector_store.py` 构建知识库
3. 执行 `streamlit run app.py` 启动应用
4. 测试普通问答，例如：
   - “扫地机器人卡在沙发底部怎么办？”
   - “小户型适合什么扫地机器人？”
5. 测试报告生成，例如：
   - “给我生成我的使用报告”

## 13. 说明

本项目当前定位为本地可运行的 LLM 应用原型，适合用于：

- 学习 Agent + Tool Calling 的基本模式
- 理解 RAG 检索增强应用结构
- 演示 Prompt 切换与运行时上下文注入
- 作为后续业务化改造的起点

