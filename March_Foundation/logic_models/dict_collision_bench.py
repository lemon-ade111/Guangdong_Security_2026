import time

# 1. 定义一个正常的类
class NormalKey:
    def __init__(self, value):
        self.value = value
    def __hash__(self):
        return hash(self.value) # 使用系统默认的哈希逻辑

# 2. 定义一个“制造冲突”的类（坏孩子）
class CollidingKey:
    def __init__(self, value):
        self.value = value
    def __hash__(self):
        return 42 # 暴力破解：无论什么内容，哈希值永远返回 42！

def benchmark(key_class, num_items, label):
    test_dict = {}
    keys = [key_class(i) for i in range(num_items)]
    
    # 测量插入时间
    start_time = time.time()
    for k in keys:
        test_dict[k] = "data"
    end_time = time.time()
    print(f"[{label}] 插入 {num_items} 个元素耗时: {end_time - start_time:.5f} 秒")

    # 测量查找时间（最核心的性能指标）
    start_time = time.time()
    for k in keys:
        _ = test_dict[k]
    end_time = time.time()
    print(f"[{label}] 查找 {num_items} 个元素耗时: {end_time - start_time:.5f} 秒")

# 执行对比实验
NUM = 100000 # 初始设置 1 万次，根据你的 Ryzen AI 9 性能可以再往上加
print(f"--- 开启哈希性能极限测试 (样本量: {NUM}) ---")
benchmark(NormalKey, NUM, "正常哈希")
benchmark(CollidingKey, NUM, "哈希冲突")