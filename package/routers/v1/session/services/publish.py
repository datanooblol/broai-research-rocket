from agents.blog_writer import BlogWriter
from package.database.session.model import SessionEnrich
from package.database.session.model import SessionStep, SessionPublish
import json


class PublishService:
    def __init__(self, sessionDB):
        self.sessionDB = sessionDB

    def publish(self, session_id: str):
        """get tone_of_voice, parsed_outline, enriched_contexts, revise, update publish, return publish"""
        blog_writer = BlogWriter()
        record = self.sessionDB.get_session(session_id).to_dict(orient="records")[0]
        tone_of_voice = record.get("tone_of_voice")
        outline = record.get("outline")
        session_enrichs = SessionEnrich(
            session_id=record.get("session_id"),
            enrich=json.loads(record.get("enrich"))
        )
        draft = []
        for section in session_enrichs.enrich.sections:
            _section = section.section
            _questions = section.questions
            draft.append(f"## {_section}")
            for question in _questions:
                _question = question.question
                _answer = question.answer
                draft.append(f"### {_question}")
                draft.append(f"{_answer}")
        draft = "\n\n".join(draft)
        request = {
            "draft": draft,
            "outline": outline,
            "message": tone_of_voice
        }
        blog_writer.run(request)
        _publish = blog_writer.output_text
        sp = SessionPublish(session_id=session_id, publish=_publish, step=SessionStep.PUBLISH)
        self.sessionDB.update_publish(sp)
        return sp