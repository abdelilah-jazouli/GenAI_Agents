from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple
from database import Database

class ConversationalAgent:
    DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."
    
    def __init__(self, 
                 system_prompt: Optional[str] = None,
                 model_name: str = "gpt-4",
                 max_tokens: int = 1000,
                 temperature: float = 0,
                 db_path: str = "conversations.db"):
        # Charger les variables d'environnement
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
        
        # Initialiser le modèle
        self.llm = ChatOpenAI(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Initialiser la base de données
        self.db = Database(db_path)
        
        # Store temporaire pour l'historique des conversations actives
        self.store = {}
        
        self.default_system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        
        # Initialiser la chaîne avec le prompt par défaut
        self._initialize_chain()

    def _initialize_chain(self, session_id: Optional[str] = None):
        """Initialise ou met à jour la chaîne avec le prompt système approprié"""
        system_prompt = self._get_system_prompt(session_id)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        chain = self.prompt | self.llm
        self.chain_with_history = RunnableWithMessageHistory(
            chain,
            self.get_chat_history,
            input_messages_key="input",
            history_messages_key="history"
        )

    def get_chat_history(self, session_id: str):
        """Récupère l'historique de chat, en le chargeant depuis la BD si nécessaire"""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
            # Charger l'historique depuis la BD
            for role, content in self.db.get_session_history(session_id):
                if role == "human":
                    self.store[session_id].add_user_message(content)
                elif role == "assistant":
                    self.store[session_id].add_ai_message(content)
        return self.store[session_id]

    def _get_system_prompt(self, session_id: Optional[str] = None) -> str:
        """Récupère le prompt système pour une session donnée"""
        if session_id:
            stored_prompt = self.db.get_system_prompt(session_id)
            return stored_prompt if stored_prompt else self.default_system_prompt
        return self.default_system_prompt

    def set_system_prompt(self, prompt: str, session_id: str):
        """Définit un prompt système personnalisé pour une session"""
        self.db.create_or_update_session(session_id, prompt)
        self._initialize_chain(session_id)

    def chat(self, message: str, session_id: str = "default_user") -> str:
        """Envoie un message et obtient une réponse"""
        # S'assurer que la session existe
        self.db.create_or_update_session(session_id, self._get_system_prompt(session_id))
        
        # Sauvegarder le message de l'utilisateur
        self.db.add_message(session_id, "human", message)
        
        # Obtenir la réponse
        response = self.chain_with_history.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Sauvegarder la réponse
        self.db.add_message(session_id, "assistant", response.content)
        
        return response.content

    def get_conversation_history(self, session_id: str = "default_user") -> List[Tuple[str, str]]:
        """Obtient l'historique de la conversation depuis la BD"""
        return self.db.get_session_history(session_id)

    def reset_conversation(self, session_id: str = "default_user"):
        """Réinitialise l'historique de la conversation"""
        if session_id in self.store:
            del self.store[session_id]
        self.db.delete_session(session_id)

    def list_sessions(self) -> List[Tuple[str, str, str]]:
        """Liste toutes les sessions disponibles"""
        return self.db.list_sessions()
