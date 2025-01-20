class LLMMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class Context:
    """
    管理LLM请求历史记录的类
    """
    def __init__(self):
        self.messages: list[LLMMessage] = []
        self.max_length = 8000
        
    def append(self, message: LLMMessage):
        """
        添加一条对话记录
        
        Args:
            message: 消息内容
        """
        
        self.messages.append(message)

    def __str__(self):
        """
        将历史记录转换为字符串
        
        Returns:
            格式化的历史记录字符串
        """
        return "User means the message from the user.\n" + \
            "Assistant means the message from the assistant or LLM.\n" + \
            "Following is the messages:\n" + "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages])
        
    def clear(self):
        """
        清空历史记录
        """
        self.messages = []


history = Context()
