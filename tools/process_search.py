def find_process(query, processes):

    query_words = query.lower().split()

    for process in processes:

        process_text = (
            process["name"] + " " +
            process["description"]
        ).lower()

        if any(word in process_text for word in query_words):
            return process

    return None