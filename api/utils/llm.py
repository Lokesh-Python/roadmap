from azure.identity import ClientSecretCredential
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from api.config import settings


def output_format(pydanticClass):
    output_parser = PydanticOutputParser(pydantic_object= pydanticClass)

    return output_parser.get_format_instructions(), output_parser

def create_template(prompt, input_variable, format_instructions):
    template = PromptTemplate(
        template=prompt, 
        input_variables=input_variable,
        partial_variables = {"format_instructions" : format_instructions})
    azurellm = create_llm()
    return template, azurellm

def create_llmChain(azurellm, template):
    chain = LLMChain(llm=azurellm, prompt= template)
    return chain

def get_result(output_parser, chain, input_dict):
    runResult = run_llmChain(chain, input_dict)
    result = output_parser.parse(runResult)
    return result

def run_llmChain(chain, input_dict):
    return chain.run(input_dict)


def create_llm():
    azurellm = AzureChatOpenAI(
        deployment_name=settings.deployment_name, model_name=settings.model_name,
        openai_api_key= settings.openai_api_token,
        openai_api_base= settings.openai_api_base,
        openai_api_type=settings.openai_api_type,
        openai_api_version=settings.openai_api_version
    )
    return azurellm

def chat_completion(parse_class, input_variable_list, prompt, dynamic_input):
    format_instructions, output_parser = output_format(parse_class)
    template, azurellm = create_template(prompt, input_variable_list, format_instructions)    
    chain = create_llmChain(azurellm, template)
    result = get_result(output_parser, chain, dynamic_input)
    return result