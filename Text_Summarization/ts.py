from summarizer import Summarizer

body = """Artificial Intelligence (AI) is revolutionizing the way we live and work. From virtual assistants like Siri and Alexa to self-driving cars and advanced medical diagnosis systems, AI technologies are becoming increasingly integrated into our daily lives. Machine learning, a subset of AI, enables computers to learn from data and improve their performance over time without explicit programming.

Deep learning, a more sophisticated form of machine learning, uses neural networks inspired by the human brain to process complex patterns and make decisions. These networks can recognize images, understand natural language, and even create art. The development of large language models like GPT-4 has demonstrated remarkable capabilities in generating human-like text, translating languages, and solving complex problems.

However, the rise of AI also brings significant challenges. Privacy concerns, ethical considerations, and potential job displacement are important issues that need to be addressed. There's also the risk of AI systems inheriting biases from their training data, which could lead to unfair or discriminatory outcomes. Additionally, the environmental impact of training large AI models is a growing concern due to their substantial energy consumption.

Despite these challenges, AI continues to advance rapidly. Researchers are working on making AI systems more transparent, fair, and energy-efficient. The development of explainable AI aims to make these systems' decision-making processes more understandable to humans. Meanwhile, edge AI is bringing AI capabilities to devices with limited computing power, making the technology more accessible and reducing reliance on cloud computing."""

model = Summarizer()
result = model(body, ratio=0.3, min_length=30, max_length=150)  # Get summary with 30% of original length

# Print the summary
print("\nOriginal Text:")
print(body)
print("\nSummarized Text:")
print(result)
