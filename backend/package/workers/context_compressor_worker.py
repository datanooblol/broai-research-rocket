from package.workers.controller import celery_app
from agents.context_compressor import ContextCompressor
import os
from uuid import uuid4
import json


@celery_app.task
def context_compressor_worker(context: str, question: str):
    request = {
        "context": context,
        "message": question
    }
    context_compressor = ContextCompressor()
    answer = context_compressor.run(request)
    return {
        "question": question,
        "answer": answer
    }