graph = {}

def check_relation(links, first_name, second_name) -> bool:
    for link in links:
        first_entity, second_entity = link
        if first_entity not in graph:
            graph[first_entity] = set()
        if second_entity not in graph:
            graph[second_entity] = set()
        graph[first_entity].add(second_entity)
        graph[second_entity].add(first_entity)
        
    visited = set()
    stack = [first_name]
    while stack:
        current_name = stack.pop()
        if current_name == second_name:
            return True
        visited.add(current_name)
        for friend in graph[current_name]:
            if friend not in visited:
                stack.append(friend)
    return False

if __name__ == '__main__':
    links = (
        ("Ваня", "Лёша"), ("Лёша", "Катя"),
        ("Ваня", "Катя"), ("Вова", "Катя"),
        ("Лёша", "Лена"), ("Оля", "Петя"),
        ("Стёпа", "Оля"), ("Оля", "Настя"),
        ("Настя", "Дима"), ("Дима", "Маша")
    )

    assert check_relation(links, "Петя", "Стёпа") is True
    assert check_relation(links, "Маша", "Петя") is True
    assert check_relation(links, "Ваня", "Дима") is False
    assert check_relation(links, "Лёша", "Настя") is False
    assert check_relation(links, "Стёпа", "Маша") is True
    assert check_relation(links, "Лена", "Маша") is False
    assert check_relation(links, "Вова", "Лена") is True
