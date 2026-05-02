"""
GeoSched 智策平台 - Mock 数据模块
数据结构已按轨道字段(orbits.zip)和前端页面设计对齐
后续算法组/数据组完成后，直接替换此文件中的数据源即可
"""

import random

# ── 任务数据（Task Data）──────────────────────────────────────────
# 字段对齐前端 data.html 任务表格
TASK_TYPES = ["光学成像", "雷达侦察", "通信中继", "气象探测", "导航增强"]
TASK_STATUS = ["待调度", "调度中", "已完成", "已取消"]

def get_tasks(count: int = 20) -> list:
    random.seed(42)
    tasks = []
    base_dates = [
        ("2025-05-12 08:00", "2025-05-12 10:00"),
        ("2025-05-12 10:30", "2025-05-12 13:00"),
        ("2025-05-13 07:00", "2025-05-13 09:30"),
        ("2025-05-13 14:00", "2025-05-13 16:00"),
        ("2025-05-14 09:00", "2025-05-14 11:30"),
        ("2025-05-14 15:00", "2025-05-14 17:00"),
        ("2025-05-15 08:30", "2025-05-15 11:00"),
        ("2025-05-16 06:00", "2025-05-16 08:00"),
        ("2025-05-17 10:00", "2025-05-17 12:30"),
        ("2025-05-18 09:00", "2025-05-18 11:00"),
    ]
    priority_weights = [1, 1, 1, 2, 2, 2, 3, 3, 3, 3]  # 1=低 2=中 3=高

    for i in range(count):
        idx = i % len(base_dates)
        priority = priority_weights[i % len(priority_weights)]
        status_idx = 0 if priority == 3 else (1 if i % 5 == 0 else 2)
        tasks.append({
            "task_id": f"TASK-{1000 + i}",
            "priority": priority,
            "start_time": base_dates[idx][0],
            "end_time": base_dates[idx][1],
            "profit": round(random.uniform(50, 500), 1),
            "energy": round(random.uniform(100, 800), 0),
            "task_type": TASK_TYPES[i % len(TASK_TYPES)],
            "status": TASK_STATUS[status_idx],
        })
    return tasks


# ── 资源数据（Satellite / Resource Data）──────────────────────────
# 字段对齐 orbits.zip 轨道参数 + 前端资源表格
# 后续可直接从 orbits.zip 中读取真实数据替换
SATELLITES = [
    {
        "sat_id": "SAT-001",
        "model": "GeoEye-A",
        "energy_available": 18560,
        "status": "在轨运行",
        "orbit_height": 500,
        "inclination": 97.35,
        "eccentricity": 0.0009909,
        "semi_major_axis": 6877000.0,
        "raan": 77.36,
        "arg_of_perigee": 119.90,
        "windows_today": 8,
        "completed_tasks": 236,
        "utilization": 82,
    },
    {
        "sat_id": "SAT-002",
        "model": "GeoEye-B",
        "energy_available": 16840,
        "status": "在轨运行",
        "orbit_height": 520,
        "inclination": 98.12,
        "eccentricity": 0.0010234,
        "semi_major_axis": 6898000.0,
        "raan": 81.22,
        "arg_of_perigee": 102.45,
        "windows_today": 6,
        "completed_tasks": 198,
        "utilization": 65,
    },
    {
        "sat_id": "SAT-003",
        "model": "RadarSat-I",
        "energy_available": 21200,
        "status": "在轨运行",
        "orbit_height": 550,
        "inclination": 53.05,
        "eccentricity": 0.0003210,
        "semi_major_axis": 6928000.0,
        "raan": 144.80,
        "arg_of_perigee": 87.33,
        "windows_today": 10,
        "completed_tasks": 312,
        "utilization": 91,
    },
    {
        "sat_id": "SAT-004",
        "model": "CommLink-II",
        "energy_available": 9800,
        "status": "维护中",
        "orbit_height": 480,
        "inclination": 42.00,
        "eccentricity": 0.0015600,
        "semi_major_axis": 6858000.0,
        "raan": 30.10,
        "arg_of_perigee": 200.11,
        "windows_today": 0,
        "completed_tasks": 87,
        "utilization": 38,
    },
    {
        "sat_id": "SAT-005",
        "model": "WeatherEye",
        "energy_available": 14300,
        "status": "在轨运行",
        "orbit_height": 600,
        "inclination": 90.00,
        "eccentricity": 0.0000500,
        "semi_major_axis": 6978000.0,
        "raan": 270.00,
        "arg_of_perigee": 0.00,
        "windows_today": 7,
        "completed_tasks": 156,
        "utilization": 54,
    },
]


# ── 调度结果 Mock（Optimize Result）──────────────────────────────
# 结构对齐 schedule.html 方案卡片和对比表
OPTIMIZE_SOLUTIONS = [
    {
        "name": "方案 A",
        "algorithm": "Proposed",
        "profit": 9128.6,
        "completion_rate": 92.4,
        "energy": 18560,
        "score": 91.6,
        "profit_rank": 1,
        "completion_rank": 1,
        "energy_rank": 2,
        "is_best": True,
        "resource_alloc": [
            {"resource": "SAT-001", "alloc_pct": 82, "utilization": 91},
            {"resource": "SAT-002", "alloc_pct": 65, "utilization": 88.6},
            {"resource": "SAT-003", "alloc_pct": 54, "utilization": 82.5},
            {"resource": "SAT-004", "alloc_pct": 38, "utilization": 75.0},
            {"resource": "SAT-005", "alloc_pct": 17, "utilization": 49.8},
        ],
    },
    {
        "name": "方案 B",
        "algorithm": "NSGA-III",
        "profit": 8732.1,
        "completion_rate": 90.3,
        "energy": 16842,
        "score": 87.4,
        "profit_rank": 2,
        "completion_rank": 3,
        "energy_rank": 1,
        "is_best": False,
        "resource_alloc": [],
    },
    {
        "name": "方案 C",
        "algorithm": "DE 优化",
        "profit": 8315.7,
        "completion_rate": 91.0,
        "energy": 17953,
        "score": 86.1,
        "profit_rank": 3,
        "completion_rank": 2,
        "energy_rank": 2,
        "is_best": False,
        "resource_alloc": [],
    },
    {
        "name": "Greedy 基线",
        "algorithm": "Greedy",
        "profit": 7256.3,
        "completion_rate": 84.6,
        "energy": 15321,
        "score": 76.2,
        "profit_rank": 4,
        "completion_rank": 4,
        "energy_rank": 1,
        "is_best": False,
        "resource_alloc": [],
    },
]

KPI_DATA = {
    "pending_tasks": 1248,
    "available_resources": 4,         # SAT-004 维护中，可用4颗
    "candidate_solutions": 36,
    "best_profit": 9128.6,
}


# ── 图表分析数据（Result / Analysis）─────────────────────────────
# 对齐 analysis.html 各图表需求

ALGO_NAMES = ["Proposed", "NSGA-III", "DE 优化", "Greedy"]

def get_result_data() -> dict:
    """返回 analysis.html 所需图表数据"""
    # 算法对比（收益/完成率/能耗）
    algo_comparison = {
        "algorithms": ALGO_NAMES,
        "profit":          [9128.6, 8732.1, 8315.7, 7256.3],
        "completion_rate": [92.4,   90.3,   91.0,   84.6],
        "energy":          [18560,  16842,  17953,  15321],
    }

    # Pareto 前沿散点数据
    random.seed(7)
    pareto_series = {}
    bases = {
        "Proposed": (1.2, 92.0),
        "NSGA-III": (1.8, 86.0),
        "DE 优化":  (2.2, 83.0),
        "Greedy":   (3.2, 75.0),
    }
    for name, (ex, ey) in bases.items():
        n = 1 if name == "Proposed" else 8
        pareto_series[name] = [
            [round(ex + (random.random() - 0.5) * (0.1 if name == "Proposed" else 0.8), 3),
             round(ey + (random.random() - 0.5) * (0.5 if name == "Proposed" else 5.0), 2)]
            for _ in range(n)
        ]

    # 关键指标摘要
    summary = {
        "best_algorithm": "Proposed",
        "profit_improvement": 12.4,   # % 相较次优
        "energy_reduction": 15.8,     # % 相较次优（注：Proposed能耗略高，此为示意）
        "coverage_improvement": 8.6,  # % 相较基线
        "best_profit": 9128.6,
        "load_balanced": True,
        "balance_improvement": 18.3,
    }

    # 甘特图数据（供 visual.html 使用）
    gantt_resources = ["SAT-001", "SAT-002", "SAT-003", "SAT-004", "SAT-005"]
    gantt_tasks = [
        [4,"2026-05-01 08:00","2026-05-01 14:30","done"],
        [4,"2026-05-01 16:00","2026-05-01 23:00","done"],
        [4,"2026-05-02 09:00","2026-05-02 21:00","done"],
        [4,"2026-05-02 22:30","2026-05-03 10:00","done"],
        [4,"2026-05-03 11:00","2026-05-03 18:30","running"],
        [4,"2026-05-03 20:00","2026-05-03 23:59","pending"],
        [3,"2026-05-01 06:00","2026-05-01 18:00","done"],
        [3,"2026-05-02 07:00","2026-05-02 15:00","done"],
        [3,"2026-05-02 16:30","2026-05-03 04:30","done"],
        [3,"2026-05-03 06:00","2026-05-03 14:00","running"],
        [3,"2026-05-03 15:30","2026-05-03 23:59","pending"],
        [2,"2026-05-01 08:00","2026-05-01 20:00","done"],
        [2,"2026-05-02 06:00","2026-05-02 18:00","done"],
        [2,"2026-05-02 20:00","2026-05-03 08:00","done"],
        [2,"2026-05-03 09:30","2026-05-03 18:00","running"],
        [2,"2026-05-03 19:00","2026-05-03 23:59","pending"],
        [1,"2026-05-01 10:00","2026-05-01 22:00","done"],
        [1,"2026-05-02 08:00","2026-05-02 18:30","done"],
        [1,"2026-05-03 07:00","2026-05-03 15:00","error"],
        [1,"2026-05-03 16:00","2026-05-03 23:59","waiting"],
        [0,"2026-05-01 12:00","2026-05-02 00:00","done"],
        [0,"2026-05-02 10:00","2026-05-02 22:00","done"],
        [0,"2026-05-03 06:00","2026-05-03 14:00","done"],
        [0,"2026-05-03 15:00","2026-05-03 23:30","running"],
    ]
    gantt_stats = {"done": 13, "running": 5, "pending": 4, "waiting": 1, "error": 1}

    return {
        "algo_comparison": algo_comparison,
        "pareto": pareto_series,
        "summary": summary,
        "gantt": {
            "resources": gantt_resources,
            "tasks": gantt_tasks,
            "stats": gantt_stats,
            "revenue": "8,732",
            "time_start": "2026-05-01",
            "time_end":   "2026-05-04",
        },
    }
