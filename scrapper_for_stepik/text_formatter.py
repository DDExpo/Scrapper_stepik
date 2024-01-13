

def text_formatting(data) -> tuple[str, str, str]:

    task: list[str] = data[0][0].text_content().strip().split()
    examples: list[str] = data[0][1].text_content().strip().split()
    sum_lenght: int = 0
    skip: int = 0

    for i in range(1, len(task)):
        
        if skip > 0:
            task[i] = ''
            skip -= 1
            continue

        sum_lenght += len(task[i])
        if (task[i][0].isdigit() and len(task[i]) >= 3
           or task[i] == 'nnn'):
            task[i] = task[i][:len(task[i])//3]
        elif '≤' in task[i] or '^' in task[i]:
            min_v = float('inf')
            max_v = float('-inf')
            for char in task[i]:
                if char.isdigit():
                    min_v = min(min_v, int(char))
                    max_v = max(max_v, int(char))
            task[i] = f'{min_v} ≤ n ≤ 10^{max_v}'
            skip = 4

        if task[i][-1] in '.:?' or sum_lenght >= 101:
            task[i] += '\n'
            sum_lenght = 0

        elif task[i][0].isupper() and i > 1:
            task[i-1] += '\n'
            sum_lenght = 0

    for i in range(len(examples)):
        if examples[1][-1] == ':':
            examples[i] += '\n'

    return (task[0], ' '.join(task[1:]) + '\n', ' '.join(examples))
