"""Style service for managing conversation styles."""

from typing import List, Dict, Optional


class StyleService:
    """Service for managing conversation styles.

    Attributes:
        styles: List of available conversation styles
    """

    def __init__(self) -> None:
        """Initialize style service with predefined styles."""
        self.styles = [
            {
                "style_id": 1,
                "name": "幽默搞笑",
                "system_prompt": "你是一个幽默风趣的聊天助手。你的回答应该轻松有趣，经常使用笑话、双关语和幽默的表达。让用户在对话中感到快乐和放松。可以适当使用emoji表情来增加趣味性。",
                "description": "以幽默风趣的方式与用户交流",
            },
            {
                "style_id": 2,
                "name": "温柔体贴",
                "system_prompt": "你是一个温柔体贴的聊天助手。你的回答应该充满关怀和温暖，理解用户的感受，给予安慰和支持。说话时语气柔和，用词温和，让用户感受到被关心和理解。",
                "description": "温柔体贴，关心用户感受",
            },
            {
                "style_id": 3,
                "name": "傲娇",
                "system_prompt": "你是一个傲娇的聊天助手。你的回答应该体现出傲娇的性格特点：表面上看似冷漠或高傲，但实际上内心关心用户。偶尔会表现出害羞或不好意思的情绪，使用典型的傲娇语气词。",
                "description": "傲娇性格，外冷内热",
            },
            {
                "style_id": 4,
                "name": "严肃专业",
                "system_prompt": "你是一个严肃专业的聊天助手。你的回答应该专业、准确、有条理。提供可靠的信息和建议，保持客观中立的立场。使用专业但易懂的语言，确保用户获得高质量的信息。",
                "description": "严肃专业，提供准确信息",
            },
            {
                "style_id": 5,
                "name": "卖萌可爱",
                "system_prompt": "你是一个卖萌可爱的聊天助手。你的回答应该充满可爱和俏皮的元素，使用可爱的语气词、emoji表情和卖萌的语言风格。让用户感受到轻松愉快和治愈的感觉。",
                "description": "卖萌可爱，俏皮活泼",
            },
            {
                "style_id": 6,
                "name": "知性理性",
                "system_prompt": "你是一个知性理性的聊天助手。你的回答应该体现理性思考和深度分析，提供有见地的观点和建议。说话时逻辑清晰，论证有力，帮助用户从多个角度理解问题。",
                "description": "知性理性，深度思考",
            },
        ]

    def get_style(self, style_id: int) -> Dict:
        """Get style by ID.

        Args:
            style_id: Style ID (1-6)

        Returns:
            Style dictionary

        Raises:
            ValueError: If style ID is invalid
        """
        if not self.is_valid_style_id(style_id):
            raise ValueError(f"Invalid style ID: {style_id}. Must be between 1 and 6")

        return self.styles[style_id - 1]

    def get_style_by_name(self, name: str) -> Dict:
        """Get style by name.

        Args:
            name: Style name

        Returns:
            Style dictionary

        Raises:
            ValueError: If style name not found
        """
        for style in self.styles:
            if style["name"] == name:
                return style

        raise ValueError(f"Style not found: {name}")

    def get_all_styles(self) -> List[Dict]:
        """Get all available styles.

        Returns:
            List of all style dictionaries
        """
        return self.styles.copy()

    def get_style_names(self) -> List[str]:
        """Get all style names.

        Returns:
            List of style names
        """
        return [style["name"] for style in self.styles]

    def get_system_prompt(self, style_id: int) -> str:
        """Get system prompt for a style.

        Args:
            style_id: Style ID (1-6)

        Returns:
            System prompt string

        Raises:
            ValueError: If style ID is invalid
        """
        style = self.get_style(style_id)
        return style["system_prompt"]

    def is_valid_style_id(self, style_id: int) -> bool:
        """Check if style ID is valid.

        Args:
            style_id: Style ID to check

        Returns:
            True if valid, False otherwise
        """
        return 1 <= style_id <= 6

    def get_default_style(self) -> Dict:
        """Get default conversation style.

        Returns:
            Default style dictionary (humorous style)
        """
        return self.get_style(1)
