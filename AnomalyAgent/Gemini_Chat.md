
**根据代理配置环境变量:**
代理location要设置的和Gemini要求的地区一样，例如：日本，英国，美国（香港不行）
```bash
export https_proxy=http://127.0.0.1:7890  http_proxy=http://127.0.0.1:7890  all_proxy=socks5://127.0.0.1:7890
```


**然后运行test：**
检查是否可以调用api，注意Gemini的role是model和user，不是assistant，system

```python
import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyC-DUwcu0XTsd-jEafCYEmlqscBsjV8DSI',transport='rest')    
model = genai.GenerativeModel('gemini-1.5-flash')    
response = model.generate_content("write a poem about the moon")    
print(response.text)
```


**下面的是Gemini的对话函数接口：**
```python
import logging
import time
import google.generativeai as genai
import os

# 配置日志
logging.basicConfig(level=logging.INFO)



# 初始化并配置模型
def initialize_model():
    """
    Initialize and configure the generative AI model with the API key.
    """
    try:
        genai.configure(api_key='AIzaSyC-DUwcu0XTsd-jEafCYEmlqscBsjV8DSI', transport='rest')
        model = genai.GenerativeModel('gemini-1.5-pro')
        return model
    except Exception as e:
        logging.error(f"Error initializing model: {e}")
        raise e

def initialize_chat(model, system_message, role='model'):
    """
    Initialize a chat session with the given system message.
    
    Parameters:
    - model: The generative AI model instance.
    - system_message: The system message to initialize the chat.
    - role: The role of the message sender ('user', or 'model').
    
    Returns:
    - chat_session: The initialized chat session.
    """
    try:
        history = [
            {
                "role": role,
                "parts": [{"text": system_message}]
            }
        ]
        return model.start_chat(history=history)
    except Exception as e:
        logging.error(f"Failed to initialize chat session: {e}")
        raise e

def send_message(chat_session, message, role='user', inline_image=None):
    """
    Send a message to the chat session and return the response.
    
    Parameters:
    - chat_session: The initialized chat session.
    - message: The text message to send.
    - role: The role of the message sender ('user' or 'model').
    - inline_image: (Optional) A dictionary containing 'mime_type' and 'data' for images.
    
    Returns:
    - response_text: The text response from the model.
    """
    try:
        if inline_image:
            parts = [
                {"text": message},
                {"inline_data": {
                    "mime_type": inline_image['mime_type'],
                    "data": inline_image['data']
                }}
            ]
            user_message = {"role": role, "parts": parts}
        else:
            user_message = {"role": role, "parts": [{"text": message}]}
        
        response = chat_session.send_message(user_message)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return f"Error: {e}"

def send_message_with_retry(chat_session, message, role='user', inline_image=None, retries=3, delay=5):
    """
    Send a message with retry logic.
    
    Parameters:
    - chat_session: The initialized chat session.
    - message: The text message to send.
    - role: The role of the message sender ('user' or 'model').
    - inline_image: (Optional) A dictionary containing 'mime_type' and 'data' for images.
    - retries: Number of retry attempts.
    - delay: Delay in seconds between retries.
    
    Returns:
    - response_text: The text response from the model or error message.
    """
    for attempt in range(1, retries + 1):
        response = send_message(chat_session, message, role, inline_image)
        if not response.startswith("Error:"):
            return response
        else:
            logging.warning(f"Attempt {attempt} failed with error: {response}")
            if attempt < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("All retry attempts failed.")
                return response

    time.sleep(1)
```
**下面的是输入图像需要对图像导入格式要做的预处理**
```python
import base64
import logging

def encode_image(image_path):
    """
    Encode an image file to a dictionary containing mime_type and Base64 data.
    
    Parameters:
    - image_path: The path to the image file.
    
    Returns:
    - A dictionary with 'mime_type' and 'data' keys.
    """
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()

        # Base64 encode the image data
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Define the mime type (you can adjust it for PNG or other formats if needed)
        mime_type = "image/jpeg"  # Change this if the image is in another format (e.g., 'image/png')

        # Return the dictionary containing mime_type and the Base64 data
        return {
            "mime_type": mime_type,
            "data": img_b64
        }
    
    except Exception as e:
        logging.error(f"Failed to encode image {image_path}: {e}")
        raise e
```
  
  <br>
  <br>   

**测试函数**
```python
import base64
import logging

def encode_image(image_path):
    """
    Encode an image file to a dictionary containing mime_type and Base64 data.
    
    Parameters:
    - image_path: The path to the image file.
    
    Returns:
    - A dictionary with 'mime_type' and 'data' keys.
    """
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()

        # Base64 encode the image data
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Define the mime type (you can adjust it for PNG or other formats if needed)
        mime_type = "image/jpeg"  # Change this if the image is in another format (e.g., 'image/png')

        # Return the dictionary containing mime_type and the Base64 data
        return {
            "mime_type": mime_type,
            "data": img_b64
        }
    
    except Exception as e:
        logging.error(f"Failed to encode image {image_path}: {e}")
        raise e

```


让GPT成为Prompt专家的Prompt：
```
I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for ChatGPT. The process is as follows: 1. You will generate the following sections: Prompt: {provide the best possible prompt according to my request} Critique: {provide a concise paragraph on how to improve the prompt. Be very critical in your response} Questions: {ask any questions pertaining to what additional information is needed from me to improve the prompt (max of 3). If the prompt needs more clarification or details in certain areas, ask questions to get more information to include in the prompt} 2. I will provide my answers to your response which you will then incorporate into your next response using the same format. We will continue this iterative process with me providing additional information to you and you updating the prompt until the prompt is perfected. Remember, the prompt we are creating should be written from the perspective of me making a request to ChatGPT. Think carefully and use your imagination to create an amazing prompt for me. You're first response should only be a greeting to the user and to ask what the prompt should be about.
```
