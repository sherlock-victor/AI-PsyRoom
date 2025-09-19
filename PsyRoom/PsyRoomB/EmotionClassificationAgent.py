import requests
import json

# 替换为你的 API_KEY 和 SECRET_KEY
API_KEY = "FSUAT3NcFgkub2ignQ9ZBie0"
SECRET_KEY = "rTDSOJBvDKR1f9XPhH3JaFBTNv9P4m45"

# 多轮咨询对话
conversation = """
你好，我是李华，很高兴认识你。今天你感觉怎么样？
你好，我是王杰。我最近心情很糟糕，特别是在工作上，感到非常嫉妒和不公平。
王杰，你能告诉我更多关于你在工作上的困扰吗？
我和同事帕特执行相同的任务，但经理对待我们很不一样。上个月帕特迟到两次，今天我们又一起迟到了，但经理对他很宽容，对我却非常严厉。我觉得很不公平，感到非常嫉妒。
听起来你对经理的态度感到很不满。你能具体描述一下经理对你们的不同对待吗？
经理对帕特说了很多关心的话，没有给他任何警告。而对我却很严厉，说这是最后一次口头警告，下次就要给我书面警告。这让我感觉很不公平。
"""

# 可选情绪类别
emotion_categories = """
可选情绪类别：
愤怒类：
- 愤怒0-面对固执己见的人
- 愤怒1-责备、诽谤和流言蜚语
- 愤怒2-欺凌、戏弄、侮辱和贬低
- 愤怒3-愚蠢和轻率的行为
- 愤怒4-驾驶情况

焦虑类：
- 焦虑0-外在因素
- 焦虑1-自我施加的压力
- 焦虑2-个人成长和人际关系
- 焦虑3-不确定性和未知数

抑郁症类：
- 抑郁症0-重要目标的失败
- 抑郁症1-亲人去世
- 抑郁症2-浪漫的失落
- 抑郁症3-慢性压力
- 抑郁症4-社交隔离
- 抑郁症5-冬天

挫败感类：
- 挫败感0-失望
- 挫败感1-不可预知的障碍和事故
- 挫败感2-沟通不畅和误解
- 挫败感3-拒绝和人际关系

嫉妒类：
- 嫉妒0-异性（同性或异性）
- 嫉妒1-物质占有
- 嫉妒2-体验式

内疚与罪恶感类：
- 内疚0-背叛与欺骗
- 罪恶感0-关系和人际交往
- 罪恶感1-违背承诺和责任
- 罪恶感2-个人和道德

恐惧类：
- 恐惧0-社交恐惧
- 恐惧1-广场恐惧
- 恐惧2-受伤
- 恐惧3-危险环境
- 恐惧4-动物

尴尬类：
- 尴尬0-亲密人
- 尴尬1-陌生人
- 尴尬2-棘手场景
- 尴尬3-焦点
"""

def get_access_token():
    """
    使用 API_KEY 和 SECRET_KEY 获取 Access Token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("获取 Access Token 失败: {}".format(response.text))

def classify_emotion(conversation, categories, access_token):
    """
    使用 API 对整体对话进行情绪分类
    """
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}"
    headers = {
        'Content-Type': 'application/json'
    }

    # 构造任务描述
    task_prompt = f"""
你是一个专业的情绪分类器。以下是一段完整的对话，请根据以下可选情绪类别选择一个最适合的情绪，并输出格式为：[主要情绪][编号]-[具体原因]。
{categories}

对话内容：
{conversation}
    """

    # 构造 payload
    payload = json.dumps({
        "messages": [
            {"role": "user", "content": task_prompt}
        ]
    }, ensure_ascii=False)

    # 调用 API
    response = requests.post(url, headers=headers, data=payload.encode("utf-8"))
    if response.status_code == 200:
        result = response.json()
        return result.get("result", "未知分类")
    else:
        raise Exception(f"API 调用失败：{response.text}")

if __name__ == '__main__':
    try:
        # 获取 Access Token
        access_token = get_access_token()
        
        # 调用情绪分类
        classification_result = classify_emotion(conversation, emotion_categories, access_token)
        
        # 输出结果
        print("情绪分类结果：", classification_result)
    except Exception as e:
        print("程序运行出错：", str(e))
