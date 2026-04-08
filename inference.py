import os
from env import CustomerSupportEnv, CustomerAction

try:
    import openai
except ImportError:
    openai = None

# --------------------------
# Configuration
# --------------------------
USE_OPENAI = False  # Keep False for reproducibility
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

if USE_OPENAI and openai and api_key:
    openai.api_key = api_key

# --------------------------
# Initialize environment
# --------------------------
env = CustomerSupportEnv()
obs = env.reset()
done = False
total_reward = 0.0

print("[START]")

while not done:
    print(f"Customer: {obs.customer_message}")

    # Default deterministic response
    ai_reply = env.conversations[env.current_index]["answer"]

    # Call OpenAI if enabled
    if USE_OPENAI and openai and api_key:
        try:
            response = openai.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant."},
                    {"role": "user", "content": obs.customer_message}
                ],
                max_tokens=100
            )
            ai_reply = response.choices[0].message.content.strip()
        except Exception as e:
            print("OpenAI API Error:", e)
            # fallback automatically

    action = CustomerAction(response_message=ai_reply, escalate_to_human=False)
    obs, reward, done, info = env.step(action)

    print(f"[STEP] AI Response: {ai_reply}")
    print(f"[STEP] Reward: {reward}\n")
    total_reward += reward

print(f"[END] Total Reward: {total_reward}")