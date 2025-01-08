import requests

base_url = "http://114.212.84.138/v1"
api_key = "app-fYF8UeUweY7Mlrg1R3YLAn3B"

def run_workflow(inputs={}, response_mode="blocking", user="default_user"):
    """
    运行工作流
    
    Args:
        inputs: 工作流输入参数字典
        response_mode: 响应模式,支持 streaming(流式)和blocking(阻塞)
        user: 用户标识
        
    Returns:
        工作流执行结果
    """
    url = f"{base_url}/workflows/run"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": inputs,
        "response_mode": response_mode,
        "user": user
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()["answer"]



def chat_message(query, inputs={}, response_mode="blocking", conversation_id="", user="default_user"):
    """
    发送聊天消息
    
    Args:
        query: 用户输入/提问内容
        inputs: 工作流输入参数字典
        response_mode: 响应模式,支持 streaming(流式)和blocking(阻塞)
        conversation_id: 会话ID
        user: 用户标识
        files: 文件列表,每个文件需包含type、transfer_method和url字段
        
    Returns:
        聊天消息响应
    """
    url = f"{base_url}/chat-messages"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": inputs,
        "query": query,
        "response_mode": response_mode,
        "conversation_id": conversation_id,
        "user": user
    }
        
    response = requests.post(url, headers=headers, json=data)
    

    return response.json()["answer"]

