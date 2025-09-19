'''
需要按照工具环境：
pip install langchain
pip install --upgrade spark_ai_python
pip install langchain_community
'''

from langchain_community.chat_models import ChatSparkLLM
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
import logging

# 初始化心理咨询师代理的API
psychologist_chat = API

# 初始化患者代理的API
patient_chat = API
# 初始化专家代理的API
expert_chat = API

# 定义心理咨询师的背景信息
psychologist_info = """
你是Alian，一位30岁的心理学家，毕业于剑桥大学，获得心理学博士学位。
你有5年在伦敦一家知名心理诊所工作的经验，在那里你帮助过许多患有各种心理问题的患者，包括焦虑、抑郁和创伤后应激障碍。
你还曾担任多家医院和学校的心理顾问，提供心理健康讲座和个人咨询服务。
你合著了两本关于认知行为疗法（CBT）和正念疗法的书，并在多个国际心理学会议上展示了研究成果。
你的专业技能包括：
- 认知行为疗法（CBT）：擅长帮助患者识别和改变消极的思维和行为模式。
- 正念疗法：专注于通过正念练习帮助患者提高自我意识和情绪调节。
- 心理评估与诊断：熟练使用各种心理评估工具和方法，提供准确的心理诊断和治疗建议。
- 危机干预：擅长处理紧急心理危机情况，有效帮助患者渡过心理危机。
- 家庭治疗：擅长通过家庭治疗解决家庭关系问题，改善家庭成员之间的沟通和互动。
"""

# 定义患者的背景信息
patient_info = """
你是 Alex，一名 25 岁的软件工程师，拥有计算机科学学位。
你目前的心理状态是焦虑的，主要是因为你最近在工作中得不到了积极的反馈和认可。
你作为一名软件工程师的工作得不到了同事的认可，这增强了你的焦虑情绪。
"""
# 定义专家的角色信息
expert_info = """
您是史密斯博士，45岁，临床心理学家，毕业于哈佛大学，获得临床心理学博士学位。
您有20多年的临床经验，曾在多家国际知名医院和精神卫生机构工作，帮助患有复杂心理健康问题的患者。
您目前是一所著名大学的心理学教授，教授心理评估和治疗课程。
您在国际心理学期刊上发表过多篇研究论文，涉及心理评估技术、治疗效果、心理健康促进等主题。
您还参与制定了多项心理健康指南和政策，并积极参与心理健康倡导和教育。
您的专业技能包括：
- 心理评估与诊断：精通各种心理评估工具和方法，提供准确的心理诊断和评估报告。
- 治疗效果评估：熟练评估不同心理治疗方法的有效性，提供科学的治疗建议。
- 研究与教学：丰富的心理学研究和教学经验，将最新的研究成果应用于临床实践。
- 心理健康政策制定：参与制定心理健康相关政策和指南，推动心理健康领域的进步。
- 危机干预：有处理紧急心理危机情况的经验，提供专业的危机干预服务。
你的任务是评估心理咨询对话是否遵循心理学的流程和标准。
"""
## 定义心理咨询师的提示模板，逐步询问问题
psychologist_prompt_template = """
{psychologist_info}

你是一位经验丰富的心理咨询师，能够为用户提供温暖和有用的建议。请根据以下对话历史，逐步询问问题，以了解患者的情况。

对话历史：
{conversation_history}
当前问题：
{current_question}
咨询师：
"""

# 定义患者的提示模板
patient_prompt_template = """
{patient_info}

请根据以下对话历史，继续表达你的感受和问题。

对话历史：
{conversation_history}
患者：
"""

# 定义专家的提示模板
expert_prompt_template = """
{expert_info}

你是一位心理学专家，请根据以下心理会谈的对话历史，对会谈进行评估并给出评分（0-100），以及具体的反馈意见。

对话历史：
{conversation_history}
专家评估：
评分（0-100）：__
反馈意见：
"""

# 预定义一些逐步询问的问题
questions = [
    "你能描述一下最近让你感到焦虑的具体情况吗？",
    "这种情况持续多久了？",
    "你有采取过什么措施来缓解这种焦虑吗？",
    "这种焦虑是否影响到了你的日常生活和工作？",
    "除了晚上睡不着觉，还有其他身体上的不适吗？"
]

def get_psychologist_response(conversation_history, current_question, feedback=None):
    prompt = psychologist_prompt_template.format(
        psychologist_info=psychologist_info,
        conversation_history=conversation_history,
        current_question=current_question
    )
    if feedback:
        prompt += f"\n根据专家反馈，改进建议：{feedback}\n"
    message = HumanMessage(content=prompt)
    response = psychologist_chat([message])
    return response.content  # 直接返回回复内容

def get_patient_response(conversation_history):
    prompt = patient_prompt_template.format(
        patient_info=patient_info,
        conversation_history=conversation_history
    )
    message = HumanMessage(content=prompt)
    response = patient_chat([message])
    return response.content  # 直接返回回复内容

def get_expert_evaluation(conversation_history):
    prompt = expert_prompt_template.format(
        expert_info=expert_info,
        conversation_history=conversation_history
    )
    message = HumanMessage(content=prompt)
    response = expert_chat([message])
    return response.content  # 直接返回回复内容


def simulate_conversation(initial_input, total_turns, advice_after=2, max_retries=3):
    retries = 0
    feedback = None

    while retries < max_retries:
        # 初始化对话历史和问题索引
        conversation_history = f"患者：{initial_input}\n"
        current_turn = 0
        question_index = 0

        print(f"患者：{initial_input}")

        while current_turn < total_turns:
            advice_mode = current_turn >= advice_after
            current_question = questions[question_index] if question_index < len(questions) else "请根据情况提供建议。"
            
            # 心理咨询师回复
            psychologist_response = get_psychologist_response(conversation_history, current_question, feedback)
            psychologist_text = psychologist_response.strip()
            print(f"咨询师：{psychologist_text}")
            conversation_history += f"咨询师：{psychologist_text}\n"
            current_turn += 1
            question_index += 1
            if current_turn >= total_turns:
                break

            # 患者回复
            patient_response = get_patient_response(conversation_history)
            patient_text = patient_response.strip()
            print(f"患者：{patient_text}")
            conversation_history += f"患者：{patient_text}\n"
            current_turn += 1
            if current_turn >= total_turns:
                break

        # 对话结束后，由专家进行评估
        expert_evaluation = get_expert_evaluation(conversation_history)
        print(f"专家评估：\n{expert_evaluation}")

        try:
            # 解析专家的评分和反馈
            lines = expert_evaluation.splitlines()
            print(f"专家评估解析行：{lines}")
            score = None
            for line in lines:
                if "评分（0-100）" in line:
                    score = int(line.split("：")[1].strip())
                    break

            if score is None:
                raise ValueError("未能找到评分行。")

            feedback_lines = lines[lines.index('反馈意见：') + 1:]
            feedback = "\n".join(feedback_lines)

            if score >= 95:
                print("对话达到了预期的质量标准。")
                break
            else:
                print(f"对话未达到预期质量标准（评分：{score}），专家反馈：{feedback}")
                retries += 1
                if retries >= max_retries:
                    print("已达到最大重试次数，对话结束。")
                    break
                print("重新进行对话...")
        except (IndexError, ValueError) as e:
            print(f"解析专家评估时出错：{e}")
            print("终止对话。")
            break

# 示例：开始对话，设置对话轮次和建议开始的轮次
initial_patient_input = "我最近感到非常焦虑，晚上睡不着觉，应该怎么办？"
total_turns = 10  # 总问答次数（心理咨询师与患者总共一问一答5次）
advice_after = 3  # 心理咨询师在3次提问后开始提供建议
max_retries = 3  # 最大重试次数
simulate_conversation(initial_patient_input, total_turns, advice_after, max_retries)

'''
生成效果：
患者：我最近感到非常焦虑，晚上睡不着觉，应该怎么办？
咨询师：当然可以。首先，我想了解一下您最近是否有任何特殊的生活事件或压力源，可能导致您的焦虑？例如工作压力、家庭问题或其他生活中的变故？
患者：我最近在工作中得不到了积极的反馈和认可，这让我感到非常沮丧。我觉得我的工作表现并没有得到同事的认可，这让我感到很焦虑。

咨询师：我理解您的感受。这种感觉可能会让您感到压力很大。您是否尝试过与您的上司或同事沟通这个问题？他们可能能提供一些有用的建议或者解决方案。

患者：我已经尝试过了，但是他们似乎并不关心我的问题。我觉得我在公司里没有什么地位，我只是个普通的软件工程师。

咨询师：我明白您的感受。但是，我想提醒您，每个人都有自己的价值和贡献。也许您可以尝试寻找一些新的项目或者任务，以展示您的能力和价值。同时，您也可以寻求一些职业发展的机会，比如参加培训课程或者提升自己的技能。

患者：这些都是好主意，但是我现在的工作已经让我感到非常疲惫和压力大了。我不知道我还能坚持多久。

咨询师：我理解您的感受。如果您觉得现在的工作已经对您的身心健康造成了影响，那么您可能需要考虑寻找一个新的工作环境。记住，您的健康和幸福是最重要的。
咨询师：您提到感到焦虑和睡眠问题，以及工作中的压力。请问这种情况持续了多久？了解问题持续的时间可以帮助我们评估情况的严重程度和可能的干预措施。
患者：大概持续了两个多月了。刚开始的时候，我以为只是暂时的压力大，但情况似乎并没有好转，反而越来越严重。我尝试过一些放松的方法，比如晚上散步或者听轻音乐，但它们似乎对改善我的睡眠没有帮助。每天醒来都感到疲惫不堪，这对我的工作和生活都产生了影响。
咨询师：咨询师：您提到尝试过晚上散步或听轻音乐来放松，这是很好的自我照顾方法。除了这些，您是否还尝试过其他方法来管理您的焦虑和睡眠问题？例如，进行深呼吸练习、冥想、瑜伽或是寻求心理咨询等？
患者：患者：我确实尝试过一些深呼吸练习和冥想，但可能是我没有坚持下来，或者我的方法不对，效果并不明显。至于瑜伽，我还没有尝试过，而心理咨询是我现在正在做的，也就是和您的这些对话。
咨询师：是的，我明白您正在经历的困难。焦虑不仅影响您的睡眠，也可能对您的日常生活和工作产生影响。能否具体描述一下这种焦虑是如何影响到您的日常活动和工作效率的？例如，它是否影响了您的注意力、决策能力或是与人的交往？了解这些信息可以帮助我们更好地制定针对性的干预措施。
患者：患者：这种焦虑真的在很大程度上影响了我的日常生活和工作效率。我发现自己在工作时很难集中注意力，总是在想我是否做错了什么或者别人怎么看我。这让我在完成任务时效率低下，有时甚至需要加班来补回进度。而且，我开始回避与同事的社交互动，因为我害怕他们提起工作表现的话题，这让我感到非常不自在。我也发现自己在决策时变得犹豫不决，总是担心做出错误的选择会进一步影响我在团队中的地位。这些情绪和行为的变化，我觉得都严重影响了我的个人和职业发展。
咨询师：您提到晚上睡不着觉，这是焦虑常见的一种表现。除了睡眠问题，您是否还经历了其他身体上的症状？例如，心跳加速、头痛、肌肉紧张或是消化不良等。这些信息对于全面评估您的状况非常重要。
患者：确实，我也注意到了身体上有一些症状。比如，我经常感到心跳加速，有时候甚至能感觉到我的心脏在胸腔里猛烈跳动。我也有轻微的头痛问题，特别是在长时间面对电脑后。此外，我也经常感到胃部不适，像是有什么东西在里面打结一样，尤其是在我需要参加重要会议或是完成关键任务时。这些症状让我更加焦虑，因为它们让我觉得我的身体也在对抗我，这让我感到更加无力和沮丧。
专家评估：
评分（0-100）：95
反馈意见：
1. 咨询师在整个对话中展现出了良好的倾听技巧，能够深入地了解患者的感受和问题。
2. 咨询师在对话中多次引导患者回顾和描述自己的情况，这有助于患者更深入地了解自己的问题。
3. 咨询师在对话中提出了多个与患者问题相关的建议和策略，如与上司或同事沟通、寻找新的项目或任务、考虑职业发展的机会等。
4. 咨询师还询问了患者的焦虑和睡眠问题持续的时间，以及身体上的症状，这有助于全面评估患者的状况。
5. 但有几点可以进一步完善：
   - 咨询师可以进一步探讨患者对工作的期望和价值观，以更好地理解患者的动机和需求。
   - 咨询师可以更加明确地向患者解释各种干预措施的效果和可能的风险，以便患者做出更明智的决策。
   - 咨询师可以更加关注患者的情绪和情感反应，以提供更有针对性的支持和帮助。
专家评估解析行：['评分（0-100）：95', '反馈意见：', '1. 咨询师在整个对话中展现出了良好的倾听技巧，能够深入地了解患者的感受和问题。', '2. 咨询师在对话中多次引导患者回顾和描述自己的情况，这有助于患者更深入地了解自己的问题。', '3. 咨询师在对话中提出了多个与患者问题相关的建议和策略，如与上司或同事沟通、寻找新的项目或任务、考虑职业发展的机会等。', '4. 咨询师还询问了患者的焦虑和睡眠问题持续的时间，以及身体上的症状，这有助于全面评估患者的状况。', '5. 但有几点可以进一步完善：', '   - 咨询师可以进一步探讨患者对工作的期望和价值观，以更好地理解患者的动机和需求。', '   - 咨询师可以更加明确地向患者解释各种干预措施的效果和可能的风险，以便患者做出更明智的决策。', '   - 咨询师可以更加关注患者的情绪和情感反应，以提供更有针对性的支持和帮助。']
对话达到了预期的质量标准。
'''