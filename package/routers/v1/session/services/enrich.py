from agents.context_compressor import ContextCompressor
from package.database.session.model import Knowledge
from package.database.session.model import (
    EnrichQuestion, EnrichSection, Enrich, SessionEnrich
)
from package.database.session.model import SessionStep
import json
from package.workers.context_compressor_worker import context_compressor_worker
from celery import group


class EnrichService:
    def __init__(self, sessionDB, knowledgeDB):
        self.sessionDB = sessionDB
        self.knowledgeDB = knowledgeDB

    def pack_context(self, contexts) -> str:
        source_list = []
        context_dict = {}
        for c in contexts:
            source = c.metadata.copy().get("source", "")
            context = c.context
            if source not in source_list:
                context_dict[source] = [f"<|start_content|>{context}<|end_content|>"]
                source_list.append(source)
            else:
                context_dict[source].append(f"<|start_content|>{context}<|end_content|>")
        prompt = []
        for s, c in context_dict.items():
            # print(s)
            context_str = "\n".join(c)
            prompt.append(
                f"SOURCE: <|start_source|>{s}<|end_source|>\nCONTENT:\n{context_str}"
            )
        return "\n\n".join(prompt)

    def enrich(self, session_id: str):
        # context_compressor_worker
        sections = Knowledge(**json.loads(
            self.sessionDB.get_session(session_id).to_dict(orient="records")[0].get("knowledge")
        ))
        question_list = []
        for section in sections.sections:
            _questions = section.questions
            for _question in _questions:
                question = _question.question
                retrieved_ids = _question.retrieved_ids
                ret_contexts = self.knowledgeDB.search_by_ids(retrieved_ids)
                context = self.pack_context(ret_contexts)
                question = question
                question_list.append({
                    "context": context, "question": question
                })
        jobs = group(context_compressor_worker.s(**sl) for sl in question_list)
        results = jobs.apply_async()
        answers = results.get()
        answer_dict = {a["question"]:a["answer"] for a in answers}

        # revise below
        section_list = []
        for section in sections.sections:
            _section = section.section
            _questions = section.questions
            enriched_question_list = []
            for _question in _questions:
                question = _question.question
                retrieved_ids = _question.retrieved_ids
                ret_contexts = self.knowledgeDB.search_by_ids(retrieved_ids)
                request = {
                    "context": self.pack_context(ret_contexts),
                    "message": question
                }
                enriched_question_list.append(
                    EnrichQuestion(question=question, answer=answer_dict[question])
                )
            section_list.append(
                EnrichSection(
                    section=_section, questions=enriched_question_list
                )
            )
        se = SessionEnrich(
            session_id=session_id,
            step=SessionStep.REVISE,
            enrich=Enrich(sections=section_list)
        )
        self.sessionDB.update_enrich(se)
        return se

    # def enrich(self, session_id: str):
    #     context_compressor = ContextCompressor()
    #     """get parsed_outline and retrieved_contexts, enrich, update enrich, return enriched_contexts"""
    #     sections = Knowledge(**json.loads(
    #         self.sessionDB.get_session(session_id).to_dict(orient="records")[0].get("knowledge")
    #     ))
    #     section_list = []
    #     for section in sections.sections:
    #         _section = section.section
    #         _questions = section.questions
    #         enriched_question_list = []
    #         for _question in _questions:
    #             question = _question.question
    #             retrieved_ids = _question.retrieved_ids
    #             ret_contexts = self.knowledgeDB.search_by_ids(retrieved_ids)
    #             request = {
    #                 "context": self.pack_context(ret_contexts),
    #                 "message": question
    #             }
    #             answer = context_compressor.run(request)
    #             enriched_question_list.append(
    #                 EnrichQuestion(question=question, answer=answer)
    #             )
    #         section_list.append(
    #             EnrichSection(
    #                 section=_section, questions=enriched_question_list
    #             )
    #         )
    #     se = SessionEnrich(
    #         session_id=session_id,
    #         step=SessionStep.REVISE,
    #         enrich=Enrich(sections=section_list)
    #     )
    #     self.sessionDB.update_enrich(se)
    #     return se