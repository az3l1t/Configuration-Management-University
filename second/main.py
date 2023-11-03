import requests
from graphviz import Digraph
#Pandas
#Requests
#Написать на выбранном вами языке программирования программу, 
# которая принимает в качестве аргумента командной строки имя пакета, 
# а возвращает граф его зависимостей в виде текста на языке Graphviz. 
# На выбор: для npm или для pip. Пользоваться самими этими менеджерами пакетов запрещено. 
# Главное, чтобы программа работала даже с неустановленными пакетами и без использования pip/npm.
def get_package_dependencies(package_name):
    url = f'https://pypi.org/pypi/{package_name}/json'
    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        dependencies = package_data['info']['requires_dist']
        return dependencies if dependencies is not None else []
    else:
        return []


def create_dependency_graph(package_name):
    graph = Digraph(package_name)
    visited = set()

    def dfs(package):
        if package in visited:
            return
        visited.add(package)
        dependencies = get_package_dependencies(package)
        for dependency in dependencies:
            dependency_package = dependency.split(' ')[0]
            graph.edge(package, dependency_package)
            dfs(dependency_package)

    dfs(package_name)
    return graph

if __name__ == '__main__':
    package_name = input('Enter package name: ')
    graph = create_dependency_graph(package_name)
    print(graph.source)

