# utils/config.py
import os
from dotenv import load_dotenv
# define workflowstate
from typing import Dict, List, Optional, TypedDict, Annotated
import operator


# define state schema for our workflow(state signature or schema that will be boradcasted)
# across various nodes of langgraph workflow
class WorkflowState(TypedDict):
	original_content: str
	instructions: str 
	current_content: str
	messages: Annotated[List, operator.add]
	writer_output: str
	reviewer_feedback: str
	manager_decision: str
	human_feedback: str
	iteration_count: int
	status: str
	metadata: dict
	quality_report: str


load_dotenv()

class Config:
	"""Configuration class for the application."""
	CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", ".TEST/chroma_db")
	GCS_BUCKET_NAME = "ai-personalized-story-templates"

	SCREENSHOTS_PATH = os.getenv("SCREENSHOTS_PATH", "./screenshots")
	
    # GCP settings
	PROJECT_ID = "bootcampai-460711"
	LOCATION = "us-central1"
	
    ## vertex AI model infos
	# MODEL_NAME = "gemini-2.0-flash"
	
	
	# OpenRouter Settings
	LLM_API_KEY : str = os.getenv("OPENROUTER_API_KEY",
							   "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"
							   #"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"
							   )

	MODEL_NAME : str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
	BASE_URL : str = os.getenv(
		"OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
	)


    # Default URLs 
	DEFAULT_URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
	
    # AI Settings
	GEMINI_OUTPUT_TOKEN_LIMIT = 8192
	MAX_TOKENS = 4000
	TEMPERATURE = 0.7
	
    # Workflow settings
	MAX_ITERATIONS = 5
	
	CHROMA_DB_PATH = "./chroma_db"

	GCP_JSON_CREDENTIALS_PATH = "gcp_json_credentials/miko3-performance-cluster-fc3d14ac2041.json"