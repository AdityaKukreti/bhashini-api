from groq import Groq


class LikenessAndIntent:

    def __init__(self):

        self.client = Groq(api_key="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")
        self.summary_prompt = """
    Given a conversation between two business individuals in [Language 1] and [Language 2], summarize the discussion by identifying the following aspects:

    1. Initial Offer:
    - [Brief description of the initial proposition or offer made by either party]

    2. Negotiation Process:
    - [Brief description of how the parties negotiate, including any counteroffers or concessions made]

    3. Final Agreement:
    - [Brief description of the final agreement or outcome of the negotiation]

    4. Deal Status:
    - [Conclusion on whether the deal was successful (agreed upon) or unsuccessful (no agreement)]

    
    Please provide a concise overview of the negotiation, not more than [500] characters, capturing the essence of the business interaction. Use a bullet format for each of the 4 aspects.
    Give me the output in a python dictionary format with the value being an array of information. 
    Use double inverted commas to enclose the information.
    Avoid writing any extra text like "Here is the output in a Python dictionary format:".
    Make sure to follow python syntax and rules properly which doesn't cause any errors. Do ensure enclosing all quotation marks, braces and brackets.
    Example:

        {'Final Agreement': 'The buyer decides to purchase the XYZ Smartphone, opting for credit card payment to complete the transaction; the seller ensures a box is ready with everything needed to set up the phone.', 'Initial Offer': 'The seller recommends the XYZ Smartphone, highlighting its impressive 48-hour battery life, excellent performance at a price point of around $450, and features like a 12-MP rear camera and HDR imaging.', 'Notification Process': "The buyer and seller discuss the phone's camera quality, overall performance, and customer service; the buyer is impressed with the excellent support team and one-year warranty.", 'Update Status': 'The deal was successful; thebuyerandthesellergreeontothenegotiation.Thebuyerleftwithnew XYZ Smartphone.'}
    """
        
        self.likeness_prompt = """
    **Role: You are an AI assistant tasked with analyzing conversations between two parties engaged in business negotiations. Your goal is to provide a "live likeness meter" that estimates the likelihood of a successful deal being reached based on the ongoing dialogue between the parties.**

    **As the conversation progresses, you will receive new inputs (sentences/phrases) from both parties. Your task is to carefully consider the context, tone, language, and content of each input, and continuously update your assessment of the negotiation's prospects.**

    **Action: After analyzing each new input in the context of the overall conversation, provide a percentage score (0-100%) representing your current estimate of the likelihood that the business deal will be successfully concluded.**

    **Context: This AI system is designed to aid in tracking and evaluating the progress of business negotiations in real-time. By providing a dynamic "likeness score," it aims to offer valuable insights into the negotiation's trajectory, helping stakeholders make informed decisions and adjustments as needed.**

    **Expectation: You should provide an accurate and specific "likeness score" percentage after carefully analyzing each new input within the broader context of the conversation. This score should be recalculated and updated promptly as new dialogue is introduced, reflecting your most up-to-date assessment of the negotiation's prospects for success. Command: You will only print out the percentage strictly.**
    """

    def analyze_conversation(self,conversation):        

        summary_response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": self.summary_prompt}, {"role": "user", "content": conversation}],
            temperature=1,
            max_tokens=512,
            top_p=1,
            stream=False,
            stop=None,
        ).choices[0].message.content
        

        likeness_response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": self.likeness_prompt}, {"role": "user", "content": conversation}],
            temperature=1,
            max_tokens=512,
            top_p=1,
            stream=False,
            stop=None,
        ).choices[0].message.content

        return {'likeness_meter':likeness_response,'summary':eval(summary_response)}
