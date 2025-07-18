from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,  AIMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from typing import List, Dict, Any
from modules.embeddings.embedding_service import EmbeddingService
from modules.langgraph.state import State
from core.dependencies.container import Container


class PromptService:
    async def general_query_prompt_template(
            self, 
            state: State
        ): 

        messages = [
            SystemMessage(content=state["system_message"]),
            SystemMessage(content="IMPORTANT! you will always respond in the language of the input")
        ]

        embeddings_service: EmbeddingService = Container.resolve("embedings_service")

        context = await embeddings_service.search_for_context(
            input=state["input"],
            agent_id=state["agent_id"],
            user_id=state["user_id"]
        )
 
        if context:
            messages.append(SystemMessage(content=f"""
                You have access to the following relevant context retrieved from documents. Use this information to inform your response. Do not make up facts outside of this context.

                Relevant context:
                {context}
            """))

        chat_history = state["chat_history"]
        
        if chat_history:
            messages = self.add_chat_history(chat_history, messages)
        
        messages.append(HumanMessagePromptTemplate.from_template('{input}'))

        prompt = ChatPromptTemplate.from_messages(messages)
        
        return prompt
    
    def add_chat_history(chat_history: List[Dict], messages: List[Any]) -> List[Any]:
        for msg in chat_history:
            if msg["sender"] == "client":
                messages.append(HumanMessage(content=msg["text"]))
            elif msg["sender"] == "agent":
                messages.append(AIMessage(content=msg["text"]))

        return messages
    
    
    