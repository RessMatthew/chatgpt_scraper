import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
def connect_to_existing_chrome():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"连接Chrome时出错: {str(e)}")
       
def call_gpt_scraper(prompt):
    """统一的GPT爬虫调用函数"""
    
    driver.get("https://chatgpt.com/")
    
    
    
    # 等待输入框加载
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "prompt-textarea"))
    )
    
    # 点击输入框使其获得焦点
    input_box.click()
    
    # 对prompt进行处理，转义特殊字符
    escaped_prompt = (prompt.replace('\\', '\\\\')
                            .replace('"', '\\"')
                            .replace("'", "\\'")
                            .replace('\n', '<br>') # 在 JavaScript 中使用 innerHTML 时，\n 会被解释为 HTML 的换行
                            .replace('\r', '\\r'))
    
    # 使用 JavaScript 设置输入框的内容
    js_code = f'document.getElementById("prompt-textarea").innerHTML = "<p>{escaped_prompt}</p>"'
    driver.execute_script(js_code)
    
    # print(f"成功输入prompt: {prompt}")
    
    # 等待发送按钮加载并点击
    send_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="send-button"]'))
    )
    send_button.click()
    
    print("已点击发送按钮")
    
    # 等待回复加载（等待语音播放按钮出现）
    voice_button = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="voice-play-turn-action-button"]'))
    )
    
    # 获取回复内容
    response_element = driver.find_element(By.CSS_SELECTOR, '.markdown.prose.w-full.break-words')
    response_text = response_element.get_attribute('outerHTML')
    
    return response_text

def alter_objectives_constraints(seed_example):
    prompt_template = """
    You are an Operations Research Engineer. Modify the given optimization problem by altering the objectives or constraints, and provide the updated problem description, AMPL code, data, and definition.

    # Original Problem Description:
    {description}

    # Original AMPL Code:
    {math_model}

    # Original Data:
    {data}

    # Original Definition:
    {definition}

    # Completion Solution:
    ## Modified Problem Description:
    (Provide updated problem description here)
    ## Modified AMPL Code:
    (Provide the updated AMPL code here)
    ## Modified Data:
    (Provide the updated data here)
    ## Modified Definition:
    (Provide the updated definition here)
    """

    # Format the input with the seed data
    prompt = prompt_template.format(
        description=seed_example["description"],
        math_model=seed_example["output"],  # Original AMPL code
        data=seed_example["data"],  # Original data
        definition=seed_example["definition"]  # Original definition
    )

    # 替换原有的OpenAI调用
    modified_result = call_gpt_scraper(prompt)
    return modified_result

def generate_expanded_scenarios(seed_example):
    prompt_template = """
    Act as an Operations Research Teacher. Create a new optimization problem based on the given scenario and question type, and generate the corresponding AMPL code, data, and definition.

    # Scenario:
    {scenario}
    # Question Type:
    {question_type}
    # Problem Description:
    {description}

    # Original Data:
    {data}

    # Original Definition:
    {definition}

    # Completion Solution:
    ## New Problem Description:
    (Provide new problem description here)
    ## New AMPL Code:
    (Provide new AMPL code here)
    ## New Data:
    (Provide new data here)
    ## New Definition:
    (Provide new definition here)
    """

    prompt = prompt_template.format(
        scenario=seed_example["scenario"],
        question_type=seed_example["type"],
        description=seed_example["description"],
        data=seed_example["data"],  # Original data
        definition=seed_example["definition"]  # Original definition
    )

    # 替换原有的OpenAI调用
    modified_result = call_gpt_scraper(prompt)
    return modified_result

def rephrase_problem_description(seed_example):
    prompt_template = """
    Rewrite the given problem description to improve clarity and readability, ensuring the mathematical model (AMPL code), data, and definition remain consistent and unchanged.

    # Original Problem Description:
    {description}

    # Original AMPL Code:
    {math_model}

    # Original Data:
    {data}

    # Original Definition:
    {definition}

    # Completion Solution:
    ## Rewritten Problem Description:
    (Provide rewritten problem description here)
    ## Unchanged AMPL Code:
    (Provide unchanged AMPL code here)
    ## Unchanged Data:
    (Provide unchanged data here)
    ## Unchanged Definition:
    (Provide unchanged definition here)
    """
    
    prompt = prompt_template.format(
        description=seed_example["description"],
        math_model=seed_example["output"],  # Original AMPL code
        data=seed_example["data"],  # Original data
        definition=seed_example["definition"]  # Original definition
    )

    # 替换原有的OpenAI调用
    modified_result = call_gpt_scraper(prompt)
    return modified_result

def apply_modeling_techniques(seed_example):
    prompt_template = """
    Enhance the given optimization problem by incorporating different modeling techniques, such as Big M method, auxiliary variables, etc., and provide the updated AMPL code, data, and definition.

    # Original Mathematical Model:
    {math_model}

    # Original Data:
    {data}

    # Original Definition:
    {definition}

    # Task: Apply different modeling techniques to enhance the model and provide updated AMPL code, data, and definition.

    # Completion Solution:
    ## Enhanced Mathematical Model:
    (Provide enhanced AMPL code here)
    ## Enhanced Data:
    (Provide enhanced data here)
    ## Enhanced Definition:
    (Provide enhanced definition here)
    """
    
    prompt = prompt_template.format(
        math_model=seed_example["output"],  # Original AMPL code
        data=seed_example["data"],  # Original data
        definition=seed_example["definition"]  # Original definition
    )

    # 替换原有的OpenAI调用
    modified_result = call_gpt_scraper(prompt)
    return modified_result

if __name__ == "__main__":    
    file_path = './datasets/fine_data.csv'
    
    # 创建result目录(如果不存在)
    if not os.path.exists('result'):
        os.makedirs('result')
    
    # 读取数据，只读取一行，跳过前两行，手动指定列名
    used = 1 + 141
    data = pd.read_csv(
        file_path,
        skiprows=1+used,
        header=None,
        names=["scenario", "type", "description", "data", "definition", "output", "answer"],
        usecols=[0, 1, 2, 3, 4, 5, 6]
        # 移除nrows=1，这样可以读取所有行
    )

    driver = connect_to_existing_chrome()
    
    for index, row in data.iterrows():
        expanded_results = []  # 移到循环内部，每次处理新行时重置
        
        # 从每一行提取数据
        seed_example = {
            "scenario": row["scenario"],
            "type": row["type"],
            "description": row["description"],
            "data": row["data"],
            "definition": row["definition"],
            "output": row["output"]
        }

        print("\n调用修改目标与约束的方法!!!\n")
        modified_result = alter_objectives_constraints(seed_example)
        print("1/4 休眠15秒...")
        time.sleep(15)
        
        print("\n调用扩展场景与问题类型的方法!!!\n")
        expanded_result = generate_expanded_scenarios(seed_example)
        print("2/4 休眠15秒...")
        time.sleep(15)
        
        print("\n调用改写问题描述的方法!!!\n")
        rephrased_result = rephrase_problem_description(seed_example)
        print("3/4 休眠15秒...")
        time.sleep(15)
        
        print("\n调用引入建模技术的方法!!!\n")
        enhanced_model_result = apply_modeling_techniques(seed_example)
        
        expanded_results.append({
            "modified": modified_result,
            "expanded": expanded_result,
            "rephrased": rephrased_result,
            "enhanced": enhanced_model_result
        })
        
        # 在每行处理完后保存结果
        expanded_results_df = pd.DataFrame(expanded_results)
        expanded_results_df.columns = ['修改后的问题', '扩展场景', '重写描述', '增强模型']
        result_filename = f'result/{index + used}.csv'
        expanded_results_df.to_csv(result_filename, index=False, encoding='utf-8')
        
        print(f"已保存结果到 {result_filename}")
        print("4/4 休眠15秒...")
        time.sleep(15)