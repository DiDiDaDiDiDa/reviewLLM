## Function Calling 的机制

原理和 Actions 一样，只是使用方式有区别。

![func](images\func.png)

Function Calling 完整的官方接口文档：https://platform.openai.com/docs/guides/function-calling

值得一提：接口里的 `tools`，最初版本叫 `functions`。这是一个很有趣的指向



## 示例 1：调用本地函数

需求：实现一个回答问题的 AI。题目中如果有加法，必须能精确计算。

 [base.py](base.py)     [math.py](math.py) 

运行结果：

![math](images\math.png)

## 示例 2：多 Function 调用

需求：查询某个地点附近的酒店、餐厅、景点等信息。即，查询某个 POI 附近的 POI。

 [local_func.py](local_func.py)     [multi_functions.py](multi_functions.py) 



结果：

![multi_functions](images\multi_functions.png)

## 示例 3：用 Function Calling 获取 JSON 结构

Function calling 生成 JSON 的稳定性比较高，因为默认启动了 [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode)。

需求：从一段文字中抽取联系人姓名、地址和电话

 [get_json.py](get_json.py) 

结果：

![get_json](images\get_json.png)



## 示例 4：通过 Function Calling 查询数据库

需求：从订单表中查询各种信息，比如某个用户的订单数量、某个商品的销量、某个用户的消费总额等等。

 [query_db.py](query_db.py) 



## 示例 5：Stream 模式

流式（stream）输出不会一次返回完整 JSON 结构，所以需要拼接后再使用。



**NLP 算法工程师视角：**

1. 模型砍大面，规则修细节
2. 一个模型搞不定的问题，拆成多个解决
3. 评估算法的准确率（所以要先有测试集，否则别问「能不能做」）
4. 评估 bad case 的影响面
5. 算法的结果永远不是100%正确的，建立在这个假设基础上推敲产品的可行性