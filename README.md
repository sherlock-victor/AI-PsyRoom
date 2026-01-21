# AI PsyRoom: A Multi-Agent Framework for AI-Driven Psychological Counseling

This repository contains the implementation and resources for the paper "AI PsyRoom: How Multi-Agent Modeling Enhances Empathetic Dialogue and Personalized Planning in AI-Driven Psychological Counseling".

## 📖 Overview

AI PsyRoom is a novel multi-agent simulation framework designed to advance AI-assisted psychological counseling. It addresses the limitations of current Large Language Models (LLMs) in understanding nuanced emotions and generating personalized, evidence-based treatment plans. The framework consists of two core components:

* **PsyRoom A**: A multi-agent system that generates high-quality, emotionally nuanced counseling dialogues.
* **PsyRoom B**: A system that utilizes the generated dialogues to create personalized and structured treatment plans.

## ✨ Key Features

* **Multi-Agent Architecture**: Utilizes specialized agents (Client, Counselor, and Professor) to simulate realistic and high-quality therapeutic conversations.
* **Fine-Grained Emotion Taxonomy**: Based on established psychological theories, our framework identifies 35 distinct sub-emotions, enabling a deeper understanding of user's emotional states.
* **Iterative Evaluation**: A "Professor" agent provides continuous feedback to refine and improve the quality of the generated dialogues.
* **EmoPsy Dataset**: A comprehensive dataset of 12,350 high-quality counseling dialogues across 423 specific scenarios.
* **Personalized Treatment Plans**: PsyRoom B generates structured and evidence-based treatment plans tailored to individual emotional needs.

## 🏛️ Framework

The AI PsyRoom framework is divided into two main parts: Data Generation and Emotional Treatment Plan Generation.

### PsyRoom A: Dialogue Generation

PsyRoom A employs a multi-agent setup to reconstruct counseling dialogues with high emotional fidelity.

1. **Raw Input**: The process starts with segmenting psychological emotions based on our detailed taxonomy.
2.  **Conversation Generation**:
    * **Client Agent**: Expresses emotions and experiences.
    * **Counselor Agent**: Provides empathetic and structured responses.
3.  **Conversation Evaluation**:
    * **Professor Agent**: Scores the dialogue based on key metrics (Problem Orientation, Compassion, Empathy, Interactive Communication) and provides feedback for iterative improvement.

### PsyRoom B: Treatment Plan Generation

PsyRoom B translates the nuanced dialogues from PsyRoom A into actionable therapeutic plans.

1. **Structured Emotional Analysis**: An Emotion Assessor agent analyzes the dialogue to identify the user's primary emotion and its triggers, outputting a structured data object.
2.  **Evidence-Based Plan Generation**: A Psychological Emotion Therapist agent uses this structured data to generate a personalized treatment plan based on evidence-based intervention strategies.

## 📊 Evaluation

Our framework has been rigorously evaluated through ablation studies, automated metrics, and human assessments. The results demonstrate significant improvements over state-of-the-art methods.

* **Dialogue Quality**: AI PsyRoom outperforms baseline models with an 18% improvement in Problem Orientation, 23% in Compassion, 24% in Empathy, and 16% in Interactive Communication.
* **Model Performance**: Our fine-tuned model, PsyRoom-8b, achieves state-of-the-art performance on key therapeutic metrics.
* **Treatment Plans**: Human evaluators, including psychology professionals, rated the treatment plans highly for their comprehensiveness, professionalism, personalization, safety, operability, and sustainability.

## Dataset

The **EmoPsy** dataset is a key contribution of this work. It contains:

* **12,350** high-quality, multi-turn counseling dialogues.
*Coverage of **35** fine-grained sub-emotions.
* **423** specific scenarios.
