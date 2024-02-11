import regex

def parse_presto_labels(sentence, target):
    # Définition du motif pour les mots, les délimiteurs et les annotations
    word_pattern = r'\p{Script=Devanagari}+|\w+|[:;][-~]?[)(]|[^\w\s]'
    double_parenthesis_pattern = r'\(\s*[^()]*\(\s*[^()]*\s*\)[^()]*\s*\)'
    annotation_pattern = r'(\w+)\s«\s([^»]+)\s»'

    # Recherche des mots dans la phrase
    words = regex.findall(word_pattern, sentence, regex.UNICODE)
    labels = [0] * len(words)

    # Vérification de la présence de deux parenthèses ouvrantes "(" consécutives avant une parenthèse fermante ")"
    double_parenthesis = regex.search(double_parenthesis_pattern, target)

    if double_parenthesis:
        # Extraction de la tâche
        task_match = regex.match(r'(\w+)', target)
        task = task_match.group(0) if task_match else ''

        # Recherche de la structure de premier niveau et des annotations
        first_level_match = regex.search(r'\(\s*(\w+)\s+\w+\s*\(', target)
        annotations = regex.findall(annotation_pattern, target)

        adjusted_annotations = []

        if first_level_match:
            first_level_key = first_level_match.group(1)

            # Préfixer chaque clé d'annotation avec le mot-clé de premier niveau
            for key, value in annotations:
                combined_key = f"{first_level_key}__{key}"
                adjusted_annotations.append((combined_key, value))
        else:
            adjusted_annotations = annotations

        # Traitement des annotations ajustées
        for key, value in adjusted_annotations:
            annotation_words = regex.findall(word_pattern, value)
            
            for i in range(len(words) - len(annotation_words) + 1):
                if words[i:i+len(annotation_words)] == annotation_words:
                    labels[i:i+len(annotation_words)] = [key] * len(annotation_words)
    else:
        # Extraction de la tâche
        task_match = regex.match(r'(\w+)', target)
        task = task_match.group(0) if task_match else ''

        # Récupération des annotations
        annotations = regex.findall(annotation_pattern, target)

        for key, value in annotations:
            nested_keys = key.split('__')
            if len(nested_keys) > 1:
                key = nested_keys[-1]

            # Traitement des annotations
            annotation_words = regex.findall(word_pattern, value)

            for i in range(len(words) - len(annotation_words) + 1):
                if words[i:i+len(annotation_words)] == annotation_words:
                    labels[i:i+len(annotation_words)] = [key] * len(annotation_words)

    return {
        "sentence": sentence,
        "words": words,
        "labels": labels,
        "task": task
    }
