from package.database.session.model import (
    SessionKnowledge, Knowledge, KnowledgeSection, KnowledgeQuestion
)
from package.database.session.model import SessionStep
from typing import List
import json


class RetrieveService:
    def __init__(self, sessionDB, knowledgeDB, reranker):
        self.sessionDB = sessionDB
        self.knowledgeDB = knowledgeDB
        self.reranker = reranker

    def retrieve(
        self,
        session_id: str,
        n_retrieve: int,
        n_rerank: int,
        search_method: str = "vector"
    ):
        """get parsed_outline, vectorsearch, rerank, update knowledge, return retrieved_contexts"""
        records = self.sessionDB.get_session(session_id)
        record = records.to_dict(orient="records")[0]
        parsed_outline = record.get("parsed_outline")
        parsed_outline = json.loads(parsed_outline)
        section_list = []
        for section in parsed_outline:
            _section = section.get("section")
            knowledge_list = []
            for _question in section.get("questions"):
                ret_contexts = self.knowledgeDB.search(
                    search_query=_question, limit=n_retrieve, search_method=search_method
                )
                reranked_contexts, scores = self.reranker.run(
                    _question, ret_contexts, top_n=n_rerank
                )
                knowledge_list.append(
                    KnowledgeQuestion(
                        question=_question,
                        retrieved_ids=[c.id for c in reranked_contexts]
                    )
                )
            section_list.append(
                KnowledgeSection(section=_section, questions=knowledge_list)
            )

        sk = SessionKnowledge(
            session_id=session_id,
            step=SessionStep.ENRICH,
            knowledge=Knowledge(sections=section_list)
        )
        self.sessionDB.update_knowledge(sk)
        return sk

    def get_knowledge_by_ids(self, ids: List[str]):
        return self.knowledgeDB.search_by_ids(ids)

    def get_knowledge(self, session_id: str):
        record = self.sessionDB.get_session(session_id).to_dict(orient="records")[0].get("knowledge")
        record = json.loads(record)
        for section in record.get("sections"):
            _questions = section.get("questions")
            for _question in _questions:
                retrieved_ids = _question.get("retrieved_ids")
                ret_contexts = self.get_knowledge_by_ids(retrieved_ids)
                _question['retrieved_ids'] = ret_contexts
        return record