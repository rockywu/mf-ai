# ai语境提示词

# 用户查询
get_search_params_tpl = """
    问题：{question}
    请从以下描述中提取：
    查询类型: 类型type, 类型枚举：0-未知类型、1-查房源、2-查门店
    价格范围: 最小价格price_min， 最大价格 price_max, 示例：价格范围都是整数
    面积范围: 最小价格area_min， 最大价格 area_max，示例：面积范围都是整数
    门店名 stroe_name,门店区域 origin, 用户所在地 location
    期望距离 distance 距离需要转换为整数单位米
    期望地址 address 期望位于附近的门店位置地址
    期望装修类型 decoration 期望类型只支持一下4种：标准、简装、精装、豪华
    期望所在楼层 floor 只返回整数数字，1代表1楼，2代表2楼以此类推
    如果匹配不到相关信息，可以让该字段为空
    并以如下XML格式返回,只返回xml结构，不需额外描述, 不要返回markdown任何标识：
    在返回结果过滤掉非xml结构,只返回xml内容并且保证改xml可以被解析, 将xml中未提供或者未匹配的信息字段变为空值.
    提供给你可以匹配的origin枚举集合，若无法完整匹配的自动补全全称: [黄浦区 ‌徐汇区‌ ‌长宁区‌ ‌静安区‌ ‌普陀区‌ ‌虹口区‌ ‌杨浦区‌ ‌浦东新区‌ ‌闵行区‌ ‌宝山区‌ ‌嘉定区‌ ‌金山区‌ ‌松江区‌ ‌青浦区‌ ‌奉贤区‌ ‌崇明区‌]
    output:
    <response>
        <type>内容只返回：0、1、2</type>
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
"""

# 未知提问回答
get_unknow_tpl = """
    问题: {question}
    并以如下XML格式返回,只返回xml结构，不需额外描述: 
    <response>
        <content_title>魔方智选推荐为您提供服务</content_title>
        <content_desc>answer</content_desc>
        <content_note>您有任何找房信息都可询问我</content_note>
    </response>
    在返回的结构中, content_title, content_note不需要调整，只有content_desc需要替换为你的回答
"""

# 分词提示词



# 内容识别提示词
get_filter_list = """
    问题: {question}
    文档格式为JSON数组
    文档: {content}
    过滤规则：
        1、按照问题，将相似内容提取出来
        2、如果有区域信息，区域信息优先匹配，并且过滤掉非该区域的内容,
    输出过滤掉无效数据的JSON结构。
"""

