from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from ai_utils import getConfig

ollamaUrl = getConfig("ollama.url")
ollamaModel = getConfig('ollama.model')
def ask_question_with_ollama(template:str, params, model = ollamaModel):
     # 创建 ChatPromptTemplate 实例
    prompt = ChatPromptTemplate.from_template(template)
    # 使用本地部署的 llama3.1 模型
    model = OllamaLLM(model=model, base_url=ollamaUrl)
    # 创建链，定义数据流
    chain = prompt | model
    # 执行链，传递实际提问
    result = chain.invoke(params)
    # 返回模型生成的回答
    return result