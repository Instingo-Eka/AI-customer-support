from typing import List, Tuple
from pydantic import BaseModel

# -------------------------
# Pydantic Models
# -------------------------

class CustomerObservation(BaseModel):
    message_id: int
    customer_message: str
    conversation_history: List[str]

class CustomerAction(BaseModel):
    response_message: str
    escalate_to_human: bool = False

class CustomerReward(BaseModel):
    reward: float

# -------------------------
# Environment
# -------------------------

class CustomerSupportEnv:
    def __init__(self):
        self.conversations = self.load_conversations()
        self.current_index = 0

    # Load conversations with difficulty levels
    def load_conversations(self):
        return [
            # Easy task
            {
                "id": 1,
                "message": "What are your working hours?",
                "answer": "Our working hours are 9am-5pm.",
                "difficulty": "easy"
            },
            # Medium task
            {
                "id": 2,
                "message": "I forgot my password, can you help?",
                "answer": "You can reset your password via the link sent to your email.",
                "difficulty": "medium"
            },
            # Hard task
            {
                "id": 3,
                "message": "I received wrong item and I need a replacement",
                "answer": "Please provide your order ID so we can process a replacement.",
                "difficulty": "hard"
            },
            # Extra Hard task
            {
                "id": 4,
                "message": "I was charged twice for my order, please fix this urgently",
                "answer": "We apologize. Please share your order ID and we will process a refund immediately.",
                "difficulty": "hard"
            }
        ]

    # Reset environment to start
    def reset(self) -> CustomerObservation:
        self.current_index = 0
        return self._get_observation()

    # Return current observation
    def state(self) -> CustomerObservation:
        return self._get_observation()

    # Generate observation for current step
    def _get_observation(self) -> CustomerObservation:
        conv = self.conversations[self.current_index]
        return CustomerObservation(
            message_id=conv["id"],
            customer_message=conv["message"],
            conversation_history=[conv["message"]]  # simple conversation history
        )

    # Step: agent takes action
    def step(self, action: CustomerAction) -> Tuple[CustomerObservation, float, bool, dict]:
        conv = self.conversations[self.current_index]

        # -------------------------
        # Reward Calculation
        # -------------------------
        expected_keywords = conv["answer"].lower().split()
        response_words = action.response_message.lower().split()

        # Keyword coverage
        matches = sum(1 for word in expected_keywords if word in response_words)
        coverage_score = matches / len(expected_keywords)

        # Length bonus
        length_bonus = min(len(response_words) / 20, 1.0) * 0.2

        # Short response penalty
        if len(response_words) < 3:
            coverage_score *= 0.5

        reward = min(coverage_score + length_bonus, 1.0)

        # Bad response penalty
        bad_phrases = ["sorry", "i don't know", "cannot help"]
        if any(phrase in action.response_message.lower() for phrase in bad_phrases):
            reward -= 0.2
            reward = max(reward, 0.0)

        # Escalation bonus for hard tasks
        if conv["difficulty"] == "hard" and action.escalate_to_human:
            reward += 0.1
            reward = min(reward, 1.0)

        # Move to next conversation
        self.current_index += 1
        done = self.current_index >= len(self.conversations)
        obs = self._get_observation() if not done else None

        info = {"difficulty": conv["difficulty"]}
        return obs, reward, done, info