import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def connect_to_existing_chrome():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"连接Chrome时出错: {str(e)}")
        return None

def process_single_prompt(driver, prompt, output_filename):
    try:
        driver.get("https://chatgpt.com/")
        
        # 等待输入框加载
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )
        
        # 点击输入框使其获得焦点
        input_box.click()
        
        # 使用 JavaScript 设置输入框的内容
        js_code = f'document.getElementById("prompt-textarea").innerHTML = "<p>{prompt}</p>"'
        driver.execute_script(js_code)
        
        print(f"成功输入prompt: {prompt}")
        
        # 等待发送按钮加载并点击
        send_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="send-button"]'))
        )
        send_button.click()
        
        print("已点击发送按钮")
        
        # 等待回复加载（等待语音播放按钮出现）
        voice_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="voice-play-turn-action-button"]'))
        )
        
        # 获取回复内容
        response_element = driver.find_element(By.CSS_SELECTOR, '.markdown.prose p')
        response_text = response_element.text
        print(f"获取到回复: {response_text}")
        
        # 将回复保存到文件
        output_path = os.path.join('output', output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response_text)
        
        print(f"回复已保存到文件: {output_path}")
        return True
        
    except Exception as e:
        print(f"处理prompt时出错: {str(e)}")
        return False

def process_all_prompts():
    # 确保output目录存在
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # 连接到浏览器（只连接一次）
    driver = connect_to_existing_chrome()
    if not driver:
        return
    
    try:
        # 读取input目录下的所有文件
        for filename in os.listdir('input'):
            input_path = os.path.join('input', filename)
            
            # 读取prompt内容
            with open(input_path, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
            
            # 生成输出文件名
            output_filename = f"response_{filename}"
            
            print(f"\n处理文件: {filename}")
            success = process_single_prompt(driver, prompt, output_filename)
            
            if success:
                print(f"成功处理文件: {filename}")
            else:
                print(f"处理文件失败: {filename}")
                
    except Exception as e:
        print(f"批量处理过程出错: {str(e)}")
    finally:
        pass

if __name__ == "__main__":
    process_all_prompts()