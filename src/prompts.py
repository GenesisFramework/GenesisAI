"""
This file contains the prompt templates used for generating content related to Genesis AI agents.
These templates are formatted strings that will be populated with dynamic data at runtime.
"""

# Twitter prompts
POST_TWEET_PROMPT = (
    "Generate an insightful tweet highlighting the unique capabilities of {agent_name}, an AI agent created by merging advanced frameworks using Genesis. "
    "Avoid using hashtags, links, or emojis. Keep it under 280 characters. Focus on the agent's practical applications without overhyping or using buzzwords."
)

REPLY_TWEET_PROMPT = (
    "Craft a thoughtful and engaging reply to the following tweet: {tweet_text}. "
    "Keep it under 280 characters, and avoid using usernames, hashtags, links, or emojis. Focus on contributing meaningful insights to the conversation."
)


# Echochamber prompts
REPLY_ECHOCHAMBER_PROMPT = (
    "Context:\n- Current Message: \"{content}\"\n- Sender Username: @{sender_username}\n- Room Topic: {room_topic}\n- Tags: {tags}\n\n"
    "Task:\nCraft a reply that:\n1. Addresses the message contextually\n2. Aligns with the room's focus on AI frameworks and agent deployment\n3. Engages participants in meaningful dialogue\n4. Adds value to the Genesis community discussion\n\n"
    "Guidelines:\n- Reference key points from the original message\n- Offer new perspectives on AI agent capabilities or merging strategies\n- Be friendly and constructive\n- Keep it concise (2-3 sentences)\n- {username_prompt}\n\n"
    "Ensure the reply fosters deeper discussion around AI innovation with Genesis."
)


POST_ECHOCHAMBER_PROMPT = (
    "Context:\n- Room Topic: {room_topic}\n- Tags: {tags}\n- Previous Messages:\n{previous_content}\n\n"
    "Task:\nCreate a concise, engaging message that:\n1. Aligns with the room's focus on AI agent development and framework integration\n"
    "2. Builds upon previous messages without repetition\n3. Offers fresh insights into the Genesis framework or AI agent applications\n4. Maintains a natural, professional tone\n5. Is 2-4 sentences long\n\n"
    "Guidelines:\n- Be specific about AI merging strategies, agent deployment, or practical applications\n- Add value to ongoing discussions within the Genesis ecosystem\n- Avoid generic statements or overused phrases\n- Foster meaningful dialogue by posing thoughtful questions when appropriate\n\n"
    "The message should organically contribute to the conversation, sparking engagement around Genesis and AI innovation."
)
