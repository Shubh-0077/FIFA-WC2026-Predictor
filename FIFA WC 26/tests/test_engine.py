from engines.group_engine import GroupEngine

sample = {
    "A": ["Mexico", "USA", "Canada", "Germany"]
}

engine = GroupEngine(sample)

result = engine.process_all_groups(sample)

print(result)