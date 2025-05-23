from broai.prompt_management.interface import Example, Examples

references = "\n".join([f"[{i+1}] Author Name {i+1}, Title {i+1}, year, referencelink {+1}" for i in range(5)])

_input1 = f"""\
Context:
SOURCE: <|start_source|>www.firstsource.com/main<|end_source|>
CONTENT:
<|start_content|>chunk 1<|end_content|>
<|start_content|>chunk 2<|end_content|>

SOURCE: <|start_source|>www.academicjournal/article/abc.pdf<|end_source|>
CONTENT:
<|start_content|>chunk 1<|end_content|>
<|start_content|>chunk 2<|end_content|>
<|start_content|>chunk 3 and some content\nReference:\n{references}<|end_content|>

SOURCE: <|start_source|>www.somerandomsource.com/index.html<|end_source|>
CONTENT:
<|start_content|>chunk 1<|end_content|>

Message:
I want to know more about something
""".strip()

_output1 = """\
Based on the provided context, It's about these ideas one [1], two [2] three [3]. The first idea is about this ...[2]. Another idea is about this [1], which is opposite to this... [2]. The final idea is this ...[3]. However all [1,2,3] agree that something and some ideas...

References:
- [1] www.academicjournal/article/abc.pdf
- [2] www.firstsource.com/main
- [3] www.somerandomsource.com/index.html
""".strip()


_input2 = f"""\
Context:

SOURCE: <|start_source|>www.academicjournal/article/abc.pdf<|end_source|>
CONTENT:
<|start_content|>This is a content [2]. According to [1,2,3,4,5], this is a content.<|end_content|>
<|start_content|>Similar to [3], this is a content [2].<|end_content|>
<|start_content|>These are summaries of some contents [2,4,5] and some content\nReference:\n{references}<|end_content|>

Message:
I want to know more about something
""".strip()
_output2 = """\
Based on the provided context, the ideas are...[1]. Another idea is about ...[1]. Some other ideas may be a couple of sentences of a short paragraph...[1].

References:
- [1] www.academicjournal/article/abc.pdf
""".strip()

examples = Examples(examples=[
    Example(
        setting="A research on a given topic",
        input=_input1,
        output=_output1,
    ),
    Example(
        setting="A research on a given topic",
        input=_input2,
        output=_output2,
    )
])