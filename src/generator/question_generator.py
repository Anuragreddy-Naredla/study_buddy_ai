#It will convert llm output into structured object
from langchain_core.output_parsers import PydanticOutputParser

from src.models.question_schemas import MCQQuestions,FillBlankQuestion
from src.prompts.templates import mcq_prompt_template,fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings_obj
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

class QuestionGenerator:
    def __init__(self):
        self.llm=get_groq_llm()
        self.loggger=get_logger(self.__class__.__name__)
    
    def _retry_and_parse(self,prompt,parser,topic,difficulty):
        for attempt in range(settings_obj.MAX_RETRIES):
            try:
                self.loggger.info(f"Generating Question for toipc {topic} with difficulty {difficulty}")
                response=self.llm.invoke(prompt.format(topic=topic,difficulty=difficulty))
                parsed=parser.parse(response.content)
                self.loggger.info("Successfully parsed the Question")
            except Exception as e:
                self.loggger.error(f"Error coming: {str(e)}")
                if attempt==settings_obj.MAX_RETRIES-1:
                    raise CustomException(f"Generation Failed after {settings_obj.MAX_RETRIES} attempts",e)
    
    def generate_mcq(self,topic,difficulty="medium") -> MCQQuestions:
        try:
            parser=PydanticOutputParser(pydantic_object=MCQQuestions)

            question=self._retry_and_parse(mcq_prompt_template,parser,topic,difficulty)

            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            self.loggger.info("Generated a valid MCQ Question")
            return question
        except Exception as e:
            self.loggger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ Generation Failed", e)
    
    def generate_fill_blank(self,topic,difficulty="medium") -> FillBlankQuestion:
        try:
            parser=PydanticOutputParser(pydantic_object=FillBlankQuestion)

            question=self._retry_and_parse(fill_blank_prompt_template,parser,topic,difficulty)
            if "___" not in question.question:
                raise ValueError("Fill in the blanks should contain '___'")
            
            self.loggger.info("Generated a valid Fill in the Blanks Question")
            return question
        except Exception as e:
            self.loggger.error(f"Failed to generate Fill up's: {str(e)}")
            raise CustomException("Fill up's Generation Failed", e)

