import random

class SearchEngine:
    def __init__(self):
        self.quest_bank = [
            {"id": 1, "task": "Drink a glass of water", "difficulty": 1},
            {"id": 2, "task": "Do 10 pushups", "difficulty": 2},
            {"id": 3, "task": "Find a blue object and take a picture", "difficulty": 2},
            {"id": 4, "task": "Solve a riddle: What has keys but can't open locks?", "difficulty": 3},
            {"id": 5, "task": "Read a page of a book", "difficulty": 1}
        ]

    def _get_neighbors(self, state):
        # A simple neighbor generation for demonstration
        return random.sample(self.quest_bank, k=min(3, len(self.quest_bank)))

    def bfs(self, start_state, target_difficulty):
        print(f"[SearchEngine] Running BFS for target difficulty {target_difficulty}")
        queue = [start_state]
        visited = set()
        
        while queue:
            current = queue.pop(0)
            if current and current.get("difficulty") == target_difficulty:
                return current
            
            # Use id or a default for hashing
            node_id = current.get("id", 0) if current else 0
            if node_id not in visited:
                visited.add(node_id)
                queue.extend(self._get_neighbors(current))
                
        return self.quest_bank[0] # Fallback

    def dfs(self, start_state, target_difficulty):
        print(f"[SearchEngine] Running DFS for target difficulty {target_difficulty}")
        stack = [start_state]
        visited = set()
        
        while stack:
            current = stack.pop()
            if current and current.get("difficulty") == target_difficulty:
                return current
                
            node_id = current.get("id", 0) if current else 0
            if node_id not in visited:
                visited.add(node_id)
                stack.extend(self._get_neighbors(current))
                
        return self.quest_bank[0]

    def astar(self, start_state, target_difficulty):
        print(f"[SearchEngine] Running A* Search for target difficulty {target_difficulty}")
        # Simplified A* where heuristic is the absolute difference in difficulty
        best_quest = min(self.quest_bank, key=lambda q: abs(q["difficulty"] - target_difficulty))
        return best_quest

    def hill_climb(self, start_state, target_difficulty):
        print(f"[SearchEngine] Running Hill Climbing for target difficulty {target_difficulty}")
        current = start_state or random.choice(self.quest_bank)
        
        for _ in range(10): # max iterations
            neighbors = self._get_neighbors(current)
            best_neighbor = min(neighbors, key=lambda q: abs(q["difficulty"] - target_difficulty))
            
            if abs(best_neighbor["difficulty"] - target_difficulty) >= abs(current.get("difficulty", 0) - target_difficulty):
                break
            current = best_neighbor
            
        return current

    def get_best_quest(self, user_state):
        # Decide difficulty based on user state (e.g. higher streak = harder)
        target_diff = 2 if user_state.get('streak_days', 0) > 3 else 1
        return self.astar(None, target_diff)
