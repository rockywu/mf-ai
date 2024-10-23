# ai语境提示词

## 生成语境提示词
def get_context_prompt(question):
    """_summary_

    Args:
        question (str): 问题描述

    Returns:
        str: 返回语境判断<xml>
    """
    return (
        f"""
        请分析以下问题，并返回其类型：
        问题：{question}
        类型包括：
            type:1;desc:查区域房源
            type:2;desc:查区域门店
            type:3;desc:查就近门店
            type:4;desc:查就近房源
            type:5;desc:未知类型
        并以如下XML格式返回,只返回xml结构，不需额外描述,返回结构中id只能是1、2、3、4、5："
        <response>
            <type>id</type>
            <desc>desc</desc>
        </response>"
        """
    )

def get_analyze_context_by_type_prompt(type: int, question):
    """
    根据类型生成分析语境提示词。

    Args:
        type (int): 问题类型 ID
        question (str): 问题描述

    Returns:
        str: 返回语境判断<xml>
    """
    if type in [1, 2, 3, 4]:
        return (
            f"""
            问题：{question}
            请从以下描述中提取：
            价格范围: 最小价格price_min， 最大价格 price_max, 示例：价格范围都是整数
            面积范围: 最小价格area_min， 最大价格 area_max，示例：面积范围都是整数
            门店名 stroe_name,门店区域 origin, 用户所在地 location
            期望距离 distance 距离需要转换为整数单位米
            期望地址 address 期望位于附近的门店位置地址
            期望装修类型 decoration 期望类型只支持一下4种：标准、简装、精装、豪华
            期望所在楼层 floor 只返回整数数字，1代表1楼，2代表2楼以此类推
            如果匹配不到相关信息，可以让该字段为空
            并以如下XML格式返回,只返回xml结构，不需额外描述：
            <response>
                <price_min>value</price_min>
                <price_max>value</price_max>
                <area_min>value</area_min>
                <area_max>value</area_max>
                <stroe_name>value</stroe_name>
                <city>value</city>
                <address>value</address>
                <origin>value</origin>
                <location>value</location>
                <decoration>value</decoration>
                <floor>value</floor>
                <distance_min>value</distance_min>
                <distance_max>value</distance_max>
            </response>
            在返回结果过滤掉非xml结构,只返回xml内容并且保证改xml可以被解析, 将xml中未提供或者未匹配的信息字段变为空值
            """
        )
    else:
        return (
            f"""
            问题: {question}
            并以如下XML格式返回,只返回xml结构，不需额外描述: 
            <response>
                <content_title>魔方智选推荐为您提供服务</content_title>
                <content_desc>answer</content_desc>
                <content_note>您有任何找房信息都可询问我</content_note>
            </response>
            在返回的结构中, content_title, content_note不需要调整，只有content_desc需要替换为你的回答
            """
        )
   
