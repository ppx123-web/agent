import os
from lambdai import AI
from dashboard import dashboard

class LLMHistory:
    """
    管理LLM请求历史记录的类
    """
    def __init__(self):
        self.messages = []
        self.max_length = 8000
        
    def append(self, message):
        """
        添加一条对话记录
        
        Args:
            message: 消息内容
        """
        dashboard.render_text(
            f"{message}",
            style="bold blue"
        )
        
        self.messages.append(message)
        
        # 如果超过最大长度,保留最新的部分
        words = " ".join(self.messages).split()
        if len(words) > self.max_length:
            # 从后往前计算保留多少条消息
            total_words = 0
            messages_to_keep = []
            for msg in reversed(self.messages):
                msg_words = len(msg.split())
                if total_words + msg_words <= self.max_length:
                    messages_to_keep.insert(0, msg)
                    total_words += msg_words
                else:
                    break
            self.messages = messages_to_keep

    def __str__(self):
        """
        将历史记录转换为字符串
        
        Returns:
            格式化的历史记录字符串
        """
        return "\n".join(self.messages)
        
    def clear(self):
        """
        清空历史记录
        """
        self.messages = []


history = LLMHistory()
