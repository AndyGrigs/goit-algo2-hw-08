import networkx as nx

def create_logistics_graph() -> nx.DiGraph:
    """
    Створює граф логістичної мережі
    """
    G = nx.DiGraph()
    
    edges = [
        # Термінал 1
        ("Термінал_1", "Склад_1", 25),
        ("Термінал_1", "Склад_2", 20),
        ("Термінал_1", "Склад_3", 15),
        
        # Термінал 2
        ("Термінал_2", "Склад_3", 15),
        ("Термінал_2", "Склад_4", 30),
        ("Термінал_2", "Склад_2", 10),
        
        # Склад 1
        ("Склад_1", "Магазин_1", 15),
        ("Склад_1", "Магазин_2", 10),
        ("Склад_1", "Магазин_3", 20),
        
        # Склад 2
        ("Склад_2", "Магазин_4", 15),
        ("Склад_2", "Магазин_5", 10),
        ("Склад_2", "Магазин_6", 25),
        
        # Склад 3 
        ("Склад_3", "Магазин_7", 20),
        ("Склад_3", "Магазин_8", 15),
        ("Склад_3", "Магазин_9", 10),
        
        # Склад 4 
        ("Склад_4", "Магазин_10", 20),
        ("Склад_4", "Магазин_11", 10),
        ("Склад_4", "Магазин_12", 15),
        ("Склад_4", "Магазин_13", 5),
        ("Склад_4", "Магазин_14", 10),
    ]
    
    # Додаємо всі ребра з пропускними здатностями
    for source, target, capacity in edges:
        G.add_edge(source, target, capacity=capacity)
    
    # Додаємо супер-джерело (SOURCE) ✅ З capacity=
    G.add_edge("SOURCE", "Термінал_1", capacity=float('inf'))
    G.add_edge("SOURCE", "Термінал_2", capacity=float('inf'))

    # Додаємо супер-стік (SINK) ✅ З capacity=
    for i in range(1, 15):
        G.add_edge(f"Магазин_{i}", "SINK", capacity=float('inf'))

    return G


def calculate_max_flow(G: nx.DiGraph) -> tuple:
    """
    Обчислює максимальний потік від SOURCE до SINK
    
    Returns:
        (max_flow_value, flow_dict) - значення потоку та розподіл по ребрах
    """
    max_flow_value, flow_dict = nx.maximum_flow(
        G, 
        "SOURCE", 
        "SINK",
        flow_func=nx.algorithms.flow.edmonds_karp
    )
    
    return max_flow_value, flow_dict

def create_terminal_to_shop_table(flow_dict: dict) -> dict:

    """
    Створює таблицю потоків від терміналів до магазинів
    
    Returns:
        dict: {(термінал, магазин): потік}
    """
    result = {}
    
    terminals = ["Термінал_1", "Термінал_2"]
    
    for terminal in terminals:
        # Потоки від термінала до складів
        if terminal not in flow_dict:
            continue
            
        for warehouse, terminal_to_warehouse_flow in flow_dict[terminal].items():
            if terminal_to_warehouse_flow == 0:
                continue
            
            # Потоки від складу до магазинів
            if warehouse not in flow_dict:
                continue
                
            # Загальний потік зі складу
            total_from_warehouse = sum(flow_dict[warehouse].values())
            
            if total_from_warehouse == 0:
                continue
            
            # Розподіляємо потік від термінала пропорційно
            for shop, warehouse_to_shop_flow in flow_dict[warehouse].items():
                if shop.startswith("Магазин") and warehouse_to_shop_flow > 0:
                    # Пропорційний розподіл
                    proportion = warehouse_to_shop_flow / total_from_warehouse
                    flow_value = terminal_to_warehouse_flow * proportion
                    
                    key = (terminal, shop)
                    if key in result:
                        result[key] += flow_value
                    else:
                        result[key] = flow_value
    
    return result

def print_results_table(terminal_shop_flows: dict):
    """
    Виводить таблицю результатів
    """
    print("\n" + "="*60)
    print("ТАБЛИЦЯ ПОТОКІВ: ТЕРМІНАЛ → МАГАЗИН")
    print("="*60)
    print(f"{'Термінал':<20} {'Магазин':<20} {'Потік (одиниць)':<20}")
    print("-"*60)
    
    for (terminal, shop), flow in sorted(terminal_shop_flows.items()):
        print(f"{terminal:<20} {shop:<20} {flow:<20.2f}")
    
    print("="*60)

def analyze_results(flow_dict: dict, terminal_shop_flows: dict, G: nx.DiGraph):
    """
    Аналізує результати та відповідає на запитання
    """
    print("\n" + "="*60)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("="*60)
    
    # ========== Питання 1 ==========
    print("\n1. Які термінали забезпечують найбільший потік товарів до магазинів?")
    terminal_totals = {}
    for (terminal, shop), flow in terminal_shop_flows.items():
        terminal_totals[terminal] = terminal_totals.get(terminal, 0) + flow
    
    for terminal, total in sorted(terminal_totals.items()):
        percentage = (total / sum(terminal_totals.values())) * 100
        print(f"   • {terminal}: {total:.2f} одиниць ({percentage:.1f}%)")
    
    max_terminal = max(terminal_totals, key=terminal_totals.get)
    print(f"   → Відповідь: {max_terminal} забезпечує найбільший потік")
    
    # ========== Питання 2 ==========
    print("\n2. Які маршрути мають найменшу пропускну здатність?")
    
    # Знаходимо всі ребра з їх пропускною здатністю та використаним потоком
    bottlenecks = []
    
    for source in flow_dict:
        if source in ["SOURCE", "SINK"]:
            continue
        for target, flow in flow_dict[source].items():
            if target in ["SOURCE", "SINK"]:
                continue
            # Отримуємо пропускну здатність з графа
            if G.has_edge(source, target):
                capacity = G[source][target]['capacity']
                utilization = (flow / capacity * 100) if capacity > 0 else 0
                bottlenecks.append((source, target, capacity, flow, utilization))
    
    # Сортуємо за пропускною здатністю
    bottlenecks.sort(key=lambda x: x[2])
    
    print("   Маршрути з найменшою пропускною здатністю:")
    for source, target, capacity, flow, util in bottlenecks[:5]:
        print(f"   • {source} → {target}: {capacity} од. (використано {flow:.1f}, {util:.1f}%)")
    
    print("\n   Вплив на загальний потік:")
    print("   → Ці маршрути обмежують можливість збільшення потоку")
    print("   → Особливо критичні повністю завантажені маршрути (100%)")
    
    # ========== Питання 3 ==========
    print("\n3. Які магазини отримали найменше товарів?")
    
    shop_totals = {}
    for (terminal, shop), flow in terminal_shop_flows.items():
        shop_totals[shop] = shop_totals.get(shop, 0) + flow
    
    # Сортуємо магазини за потоком
    sorted_shops = sorted(shop_totals.items(), key=lambda x: x[1])
    
    print("   Магазини з найменшим постачанням:")
    for shop, total in sorted_shops[:5]:
        print(f"   • {shop}: {total:.2f} одиниць")
    
    print("\n   Можливості збільшення постачання:")
    # Перевіряємо, чи є невикористана пропускна здатність
    for shop, total in sorted_shops[:3]:
        print(f"   • {shop}:")
        # Знаходимо склади, що постачають цей магазин
        for source in flow_dict:
            if source.startswith("Склад") and shop in flow_dict[source]:
                if G.has_edge(source, shop):
                    capacity = G[source][shop]['capacity']
                    flow = flow_dict[source][shop]
                    unused = capacity - flow
                    if unused > 0:
                        print(f"     - Можна збільшити від {source} на {unused:.1f} од.")
    
    # ========== Питання 4 ==========
    print("\n4. Чи є вузькі місця (bottlenecks)?")
    
    # Знаходимо повністю завантажені ребра
    fully_utilized = []
    for source, target, capacity, flow, util in bottlenecks:
        if util >= 99.9:  # Практично 100%
            fully_utilized.append((source, target, capacity))
    
    if fully_utilized:
        print("   Знайдено вузькі місця (завантажені на 100%):")
        for source, target, capacity in fully_utilized:
            print(f"   • {source} → {target} ({capacity} од.)")
        
        print("\n   Рекомендації для покращення:")
        print("   ✓ Збільшити пропускну здатність цих маршрутів")
        print("   ✓ Додати альтернативні шляхи доставки")
        print("   ✓ Перерозподілити потоки через менш завантажені маршрути")
    else:
        print("   Критичних вузьких місць не виявлено")
        print("   Мережа працює з резервом пропускної здатності")


def main():
    """
    Головна функція для запуску програми
    """
    print("="*60)
    print("ОПТИМІЗАЦІЯ ЛОГІСТИЧНОЇ МЕРЕЖІ")
    print("Алгоритм Едмондса-Карпа")
    print("="*60)
    
    # 1. Створюємо граф
    G = create_logistics_graph()
    print(f"\nГраф створено: {G.number_of_nodes()} вершин, {G.number_of_edges()} ребер")
    
    # 2. Обчислюємо максимальний потік
    max_flow_value, flow_dict = calculate_max_flow(G)
    print(f"\nМаксимальний потік: {max_flow_value:.2f} одиниць")
    
    # 3. Створюємо таблицю
    terminal_shop_flows = create_terminal_to_shop_table(flow_dict)
    
    # 4. Виводимо таблицю
    print_results_table(terminal_shop_flows)
    
    # 5. Аналіз
    analyze_results(flow_dict, terminal_shop_flows, G)

if __name__ == "__main__":
    main()