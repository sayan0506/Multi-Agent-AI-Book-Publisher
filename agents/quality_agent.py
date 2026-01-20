# AI Book Publication
# This agent will be used to check final quality of the book before publishing
from google import genai
from utils.config import Config, WorkflowState 
from google.genai.types import GenerateContentConfig
from langchain_core.messages import AIMessage, HumanMessage
from openai import OpenAI
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityAgent:
    def __init__(self):
        self.config = Config()
        # self.generation_config = GenerateContentConfig(
        #     temperature=self.config.TEMPERATURE,
        #     max_output_tokens=self.config.GEMINI_OUTPUT_TOKEN_LIMIT
        # )
        # self.client = genai.Client(
        #     project=self.config.PROJECT_ID,
        #     location=self.config.LOCATION,
        #     vertexai=True
        # )

        self.client = OpenAI(
            api_key = self.config.LLM_API_KEY, 
            base_url = self.config.BASE_URL,
        )

        self.model = self.config.MODEL_NAME

    def check_quality(self, state: WorkflowState)-> WorkflowState:
        """
        Final quality check for the book.
        """
        
        print(f"====> Checking Quality of the book...")

        try:
            prompt = f"""
            You are a Literature Quality Expert, perform a final quality check on this book. 
            Check for:
            
            1. Grammar and spelling errors
            2. Consistency issues
            3. Overall readability
            4. Content completeness
            
            Final Content:
            {state['current_content']}

            Provide a final quality score (1-10) and brief summary as quality report.
            
            """
            # as we are using async then need to use await keyword before client call
            # quality_report = self.client.models.generate_content(
            #     model=self.config.MODEL_NAME,
            #     contents=[prompt],
            #     config=self.generation_config

            # )

            quality_report = self.client.chat.completions.create(
                model = self.config.MODEL_NAME,
                messages = [
                    {
                        "role": "system",
                        "content": "You are a creative quality analyst working for book publications"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens = self.config.MAX_TOKENS,
                temperature = self.config.TEMPERATURE
            )

            quality_report = quality_report.choices[0].message.content

            logger.info(f"Quality Report: {quality_report}")

            return {
                **state,
                "quality_report": quality_report, #quality_report.text,
                "messages": state.get("messages",[])+[AIMessage(content="Quality Check Completed!")],
                "status": "completed",
            }
        
        except Exception as e:
            return {
                **state,
                "messages": state.get("messages",[])+[AIMessage(content=f"Quality Check error - {e}!")],
                "status": "quality_error",
            }


# #### FOR TESTING PURPOSES ONLY ####
# if __name__ == "__main__":
#    # Example usage
#     quality = QualityAgent()

#     # Sample input
#     original_text = (
#         "The sun was setting behind the hills as the village slowly came to life. "
#         "Children ran across the fields while elders sat outside, sharing stories from the past."
#     )

#     spun_content = (
#         """As twilight painted the hills with fire, the village stirred from its slumber.\n 
#         A tapestry of laughter unfurled as children, like dandelion seeds on the wind, scattered across emerald fields.\n 
#         Meanwhile, beneath the eaves of time-worn homes, elders gathered, their voices weaving tales of yesteryear, each word a thread in the rich fabric of memory."""
#     )
    
#     state: WorkflowState = {
#         "original_content": original_text,
#         "current_content": spun_content,
#         "messages": [],
#         "reviewer_feedback": "",
#         "manager_decision": "",
#         "iteration_count": 1,
#         "status": "",
#         "metadata": {},
#     }

#     result = quality.check_quality(state)

#     print(result['quality_report']) 