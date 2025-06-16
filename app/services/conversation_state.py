#in-memory state management for conversation context

class ConversationState:
    def __init__(self):
        self.user_states = {}  # user_id -> state dict

    def get_state(self, user_id: str) -> dict:
        if user_id not in self.user_states:
            self.user_states[user_id] = {
                "awaiting_product_selection": False,
                "awaiting_browse_confirmation": False,
                "last_products_shown": [],
                "last_intent": None
            }
        return self.user_states[user_id]

    def clear_state(self, user_id: str):
        if user_id in self.user_states:
            self.user_states[user_id] = {
                "awaiting_product_selection": False,
                "awaiting_browse_confirmation": False,
                "last_products_shown": [],
                "last_intent": None
            }
