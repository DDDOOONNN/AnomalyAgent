from chat_functions import initialize_model, initialize_chat, send_message
from image_encoder import encode_image

# 测试程序
def test_chat():
    # 初始化模型
    model = initialize_model()

    # 系统消息（可以根据需要调整）
    system_message = "You're an expert in quality anomaly detection"

    # 初始化聊天会话
    chat_session = initialize_chat(model, system_message, role='model')

    # 模拟与模型的互动
    messages = [
        "Your name is Davy.",
        "What's your name?"
    ]
    
    # for message in messages:
    #     response = send_message(chat_session, message, role='user')
    #     logging.info(f"User: {message}")
    #     logging.info(f"Model: {response}")

    image_path1 = "/Users/renjunnan/Documents/AnomalyAgent/pcb1/normal/0000.JPG"
    encoded_image1 = encode_image(image_path1)
    message1 = "This is a high-quality PCB, please remember the appearance of this PCB, and then I want you to check some PCBS."
    response1 = send_message(chat_session, message1, role='user', inline_image=encoded_image1)
    print(response1)

    image_path2 = "/Users/renjunnan/Documents/AnomalyAgent/pcb1/bad/001.JPG"
    message2 = "Compare the provided PCB image with the reference high-quality PCB image from prior context. Identify all areas where the two images differ. Highlight the regions with differences, and provide the four coordinates (x1, y1, x2, y2) of a bounding box around each differing area in JSON format. The bounding boxes should accurately cover the areas where differences are present. If there are no significant differences, return an empty list. Each differing region should be numbered sequentially (e.g., '1', '2', etc.), starting from the top-left to bottom-right of the image."
    encoded_image2 = encode_image(image_path2)
    response2 = send_message(chat_session, message2, role='user', inline_image=encoded_image2)
    print(response2)

# 运行测试程序
if __name__ == "__main__":
    test_chat()
