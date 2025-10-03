def ask_question(retriever, question, llm, prompt):
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    prompt_text = prompt.format(context=context, question=question)
    result = llm.invoke(prompt_text)
    return result.content
