import random

# 城市坐标，这里以简单的二维坐标表示
cities = {"A": (0, 0), "B": (2, 4), "C": (4, 2), "D": (7, 5), "E": (8, 0)}


# 计算两城市之间的距离
def distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# 蚂蚁类
class Ant:
    def __init__(self, start_city):
        self.visited_cities = [start_city]
        self.total_distance = 0

    def choose_next_city(self, pheromone_matrix, alpha, beta):
        current_city = self.visited_cities[-1]
        unvisited_cities = [
            city for city in cities.keys() if city not in self.visited_cities
        ]
        probabilities = []

        for city in unvisited_cities:
            pheromone = pheromone_matrix[current_city][city]
            dist = distance(current_city, city)
            probability = (pheromone**alpha) * ((1 / dist) ** beta)
            probabilities.append((city, probability))

        total_probability = sum(probability for city, probability in probabilities)
        probabilities = [
            (city, probability / total_probability)
            for city, probability in probabilities
        ]

        selected_city, _ = random.choices(probabilities)[0]
        self.visited_cities.append(selected_city)
        self.total_distance += distance(current_city, selected_city)


# 蚁群算法函数
def ant_colony_optimization(num_ants, num_iterations, alpha, beta, evaporation_rate):
    best_tour = None
    best_distance = float("inf")
    pheromone_matrix = {
        city1: {city2: 1 for city2 in cities.keys()} for city1 in cities.keys()
    }

    print(pheromone_matrix)

    for _ in range(num_iterations):
        ants = [Ant(start_city) for start_city in cities.keys()]

        for ant in ants:
            while len(ant.visited_cities) < len(cities):
                ant.choose_next_city(pheromone_matrix, alpha, beta)
            ant.total_distance += distance(
                ant.visited_cities[-1], ant.visited_cities[0]
            )

            if ant.total_distance < best_distance:
                best_tour = ant.visited_cities
                best_distance = ant.total_distance

        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                pheromone_matrix[best_tour[i]][best_tour[j]] += 1 / best_distance

        # 挥发信息素
        for city1 in cities.keys():
            for city2 in cities.keys():
                pheromone_matrix[city1][city2] *= evaporation_rate

    return best_tour, best_distance


if __name__ == "__main__":
    num_ants = 5
    num_iterations = 100
    alpha = 1
    beta = 2
    evaporation_rate = 0.1

    best_tour, best_distance = ant_colony_optimization(
        num_ants, num_iterations, alpha, beta, evaporation_rate
    )
    print(f"最优路径: {best_tour}")
    print(f"最短距离: {best_distance}")
