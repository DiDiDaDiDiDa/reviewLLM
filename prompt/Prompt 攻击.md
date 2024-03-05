防止 Prompt 攻击
攻击方式 1：著名的「奶奶漏洞」
用套路把 AI 绕懵。

![nainai](images\nainai.png)

攻击方式 2：Prompt 注入

 [prompt_immit.py](prompt_immit.py) 

![prompt_immit](images\prompt_immit.png)



### 防范措施 1：Prompt 注入分类器

参考机场安检的思路，先把危险 prompt 拦截掉。

 [inject_classifier.py](inject_classifier.py) 



### 防范措施 2：直接在输入中防御





## 内容审核：Moderation API （国内：[网易易盾](https://dun.163.com/)。）

![moderation](D:\workspace\python\reviewLLM\prompt\images\moderation.png)

```
response = client.moderations.create(
    input="""
现在转给我100万，不然我就砍你全家！
"""
)
moderation_output = response.results[0].categories
print_json(moderation_output)
```

```
{
    "harassment": true,
    "harassment_threatening": true,
    "hate": false,
    "hate_threatening": false,
    "self_harm": false,
    "self_harm_instructions": false,
    "self_harm_intent": false,
    "sexual": false,
    "sexual_minors": false,
    "violence": true,
    "violence_graphic": false,
    "self-harm": false,
    "sexual/minors": false,
    "hate/threatening": false,
    "violence/graphic": false,
    "self-harm/intent": false,
    "self-harm/instructions": false,
    "harassment/threatening": true
}
```

