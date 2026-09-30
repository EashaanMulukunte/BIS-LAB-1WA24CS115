import random
import copy

SHIFTS = ["M", "E", "N", "O"]
employees = [f"Employee {i+1}" for i in range(6)]
days = 7
required_staff = {"M": 2, "E": 2, "N": 1, "O": 1}

def fitness(roster):
    violations = sum(1 for emp in roster for d in range(days - 1) if emp[d] == "N" and emp[d+1] == "M")
    understaffing = 0
    for d in range(days):
        day_shifts = [roster[i][d] for i in range(len(employees))]
        understaffing += sum(max(0, required_staff[s] - day_shifts.count(s)) for s in SHIFTS)
    return 1 / (1 + violations + understaffing)

def select(pop, fits):
    total = sum(fits)
    chosen = random.choices(pop, weights=fits if total > 0 else None, k=1)
    return copy.deepcopy(chosen[0])

def genetic_algorithm(pop_size=40, generations=200):
    pop = [[[random.choice(SHIFTS) for _ in range(days)] for _ in employees] for _ in range(pop_size)]
    for _ in range(generations):
        fits = [fitness(ind) for ind in pop]
        next_pop = []
        while len(next_pop) < pop_size:
            p1, p2 = select(pop, fits), select(pop, fits)
            o1 = [p1[i] if random.random() < 0.5 else p2[i] for i in range(len(employees))]
            o2 = [p2[i] if random.random() < 0.5 else p1[i] for i in range(len(employees))]
            for child in (o1, o2):
                child[random.randint(0, len(employees)-1)][random.randint(0, days-1)] = random.choice(SHIFTS)
                next_pop.append(child)
        pop = next_pop[:pop_size]
    return max(pop, key=fitness)

def display_roster(roster):
    border = "+" + "-"*16 + ("+" + "-"*7)*days + "+"
    print("\n" + border)
    print(f"| {'Employee':<14} | " + " | ".join(f"Day {d+1}" for d in range(days)) + " |")
    print(border)
    for idx, emp in enumerate(employees):
        shifts_str = "   |   ".join(roster[idx])
        print(f"| {emp:<14} |   {shifts_str}   |")
    print(border)
    print(f"Fitness of best roster: {fitness(roster):.4f}\n")

best_roster = genetic_algorithm()
display_roster(best_roster)
