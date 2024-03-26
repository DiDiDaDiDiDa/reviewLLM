## 维护一个生产级的 LLM 应用，我们需要做什么？

1. 各种指标监控与统计：访问记录、响应时长、Token用量、计费等等
2. 调试 Prompt
3. 测试/验证系统的相关评估指标
4. 数据集管理（便于回归测试）
5. Prompt 版本管理（便于升级/回滚）



## 两个生产级 LLM App 维护平台

1. 重点讲解 **LangFuse**: 开源 + SaaS（免费/付费），LangSmith 平替，可集成 LangChain 也可直接对接 OpenAI API；
2. 简单讲解 **LangSmith**: LangChain 的官方平台，SaaS 服务（付费），非开源；