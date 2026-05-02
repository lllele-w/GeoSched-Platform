"""
GeoSched 智策平台 - 后端主程序
FastAPI + CORS
运行方式：uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
import csv
import os

from mock_data import get_tasks, SATELLITES, OPTIMIZE_SOLUTIONS, KPI_DATA, get_result_data

# ── CSV 数据路径（相对于 backend/ 的上级目录）──────────────────────
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TASKS_CSV     = os.path.join(_BASE_DIR, "data", "processed", "tasks_1000.csv")
_RESOURCES_CSV = os.path.join(_BASE_DIR, "data", "processed", "satellites_20.csv")


def _load_csv(path: str) -> list:
    """读取 CSV 文件，返回字典列表；文件不存在时返回空列表"""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

# ── 应用初始化 ────────────────────────────────────────────────────
app = FastAPI(
    title="GeoSched 智策平台 API",
    description="多源数据驱动的智能调度与辅助决策系统后端接口",
    version="1.0.0",
)

# ── CORS 配置（允许前端本地 file:// 及 localhost 访问）────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 开发阶段全开，上线再收紧
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求体模型 ────────────────────────────────────────────────────
class OptimizeRequest(BaseModel):
    algorithm: str = "proposed"           # proposed | nsga3 | de | greedy
    weight_profit: float = 0.5
    weight_completion: float = 0.3
    weight_energy: float = 0.2
    date_from: str = "2025-05-12"
    date_to: str = "2025-05-18"
    task_scope: str = "全部任务"
    resource_constraint: str = "默认资源约束"
    keep_elite: bool = True
    compare_mode: bool = True


# ════════════════════════════════════════════════════════════════
# GET /ping  —— 测试后端是否启动
# ════════════════════════════════════════════════════════════════
@app.get("/ping", summary="心跳检测")
def ping():
    """返回后端运行状态"""
    return {
        "status": "ok",
        "message": "GeoSched 后端服务运行正常",
        "version": "1.0.0",
        "timestamp": int(time.time()),
    }


# ════════════════════════════════════════════════════════════════
# GET /load_data  —— 返回任务数据与资源数据
# ════════════════════════════════════════════════════════════════
@app.get("/load_data", summary="加载任务与资源数据")
def load_data(count: int = 20):
    """
    返回当前批次的任务列表和卫星资源列表。

    - **count**: 返回任务条数，默认 20，最大 200
    - 数据来源：优先读取 data/processed/ 下的 CSV 文件；
      CSV 不存在时自动降级为 mock_data.py 中的模拟数据
    """
    if count > 1000:
        raise HTTPException(status_code=400, detail="count 最大值为 1000")

    # ── 读任务数据 ────────────────────────────────────────────────
    csv_tasks = _load_csv(_TASKS_CSV)
    if csv_tasks:
        # CSV 字段统一为字符串，把数值字段转换一下
        tasks = []
        for row in csv_tasks[:count]:
            tasks.append({
                "task_id":    row["task_id"],
                "priority":   int(row["priority"]),
                "start_time": row["start_time"],
                "end_time":   row["end_time"],
                "profit":     float(row["profit"]),
                "energy":     float(row["energy"]),
                "task_type":  row["task_type"],
                "status":     row["status"],
            })
        data_source = "csv"
    else:
        # 降级：使用 mock_data
        tasks = get_tasks(count)
        data_source = "mock"

    # ── 读资源数据 ────────────────────────────────────────────────
    csv_resources = _load_csv(_RESOURCES_CSV)
    if csv_resources:
        satellites = []
        for row in csv_resources:
            satellites.append({
                "sat_id":             row["sat_id"],
                "model":              row["model"],
                "energy_available":   float(row["energy_available_Wh"]),
                "status":             row["status"],
                "orbit_height":       float(row["orbit_height_m"]),
                "inclination":        float(row["inclination_deg"]),
                "eccentricity":       float(row["eccentricity"]),
                "semi_major_axis":    float(row["semi_major_axis"]),
                "raan":               float(row["raan"]),
                "arg_of_perigee":     float(row["arg_of_perigee"]),
                "windows_today":      int(row["windows_today"]),
                "completed_tasks":    int(row["completed_tasks"]),
                "utilization":        float(row["utilization"]),
                "task_type":          row["task_type"],
                "total_profit":       float(row["total_profit"]),
                "total_task_number":  int(row["total_task_number"]),
            })
    else:
        satellites = SATELLITES

    # ── 统计摘要 ──────────────────────────────────────────────────
    high_priority = sum(1 for t in tasks if t["priority"] == 3)

    return {
        "status": "ok",
        "data_source": data_source,
        "data": {
            "tasks": tasks,
            "task_summary": {
                "total": len(tasks),
                "high_priority": high_priority,
            },
            "satellites": satellites,
            "satellite_summary": {
                "total": len(satellites),
                "online": sum(1 for s in satellites if s["status"] in ("operational", "在轨运行", "服务中")),
            },
        },
    }


# ════════════════════════════════════════════════════════════════
# POST /optimize  —— 接收调度参数，返回调度结果
# ════════════════════════════════════════════════════════════════
@app.post("/optimize", summary="执行智能调度")
def optimize(req: OptimizeRequest):
    """
    接收调度参数，运行优化算法，返回多套调度方案。

    - 当前为 Mock 结果（结构完整）
    - 后续算法组完成 model.py 后，此处调用真实算法
    """
    # 参数校验
    weight_sum = round(req.weight_profit + req.weight_completion + req.weight_energy, 4)
    if not (0.99 <= weight_sum <= 1.01):
        raise HTTPException(
            status_code=400,
            detail=f"三个权重之和应为 1.0，当前为 {weight_sum}"
        )

    # 根据算法选择过滤/排序方案
    algo_map = {
        "proposed": "Proposed",
        "nsga3":    "NSGA-III",
        "de":       "DE 优化",
        "greedy":   "Greedy",
    }
    selected_algo = algo_map.get(req.algorithm.lower(), "Proposed")

    # 若指定了具体算法，把该算法的方案排到第一
    solutions = sorted(
        OPTIMIZE_SOLUTIONS,
        key=lambda s: (0 if s["algorithm"] == selected_algo else 1, -s["profit"])
    )

    best = next((s for s in solutions if s["is_best"]), solutions[0])

    return {
        "status": "ok",
        "request": {
            "algorithm": req.algorithm,
            "weights": {
                "profit":      req.weight_profit,
                "completion":  req.weight_completion,
                "energy":      req.weight_energy,
            },
            "date_range": f"{req.date_from} ~ {req.date_to}",
        },
        "data": {
            "kpi": KPI_DATA,
            "solutions": solutions,
            "best": best,
            "total_solutions": len(solutions),
        },
    }


# ════════════════════════════════════════════════════════════════
# GET /result  —— 返回分析图表所需数据
# ════════════════════════════════════════════════════════════════
@app.get("/result", summary="获取分析图表数据")
def result():
    """
    返回结果分析页所需的全部图表数据：
    - 算法对比柱状图数据（收益 / 完成率 / 能耗）
    - Pareto 前沿散点数据
    - 关键指标摘要
    """
    return {
        "status": "ok",
        "data": get_result_data(),
    }
