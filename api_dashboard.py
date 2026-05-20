from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Instantiate core FastAPI application framework configuration
app = FastAPI(
    title="Agile Sprint Analytics Engine",
    description="Production-tier REST API designed to ingest agile workflow payloads and calculate performance metrics.",
    version="1.0.0"
)


# ==========================================
# 1. DATA PARSING & VALIDATION STRUCTS (Pydantic)
# ==========================================
class Task(BaseModel):
    task_id: str
    title: str
    status: str = Field(..., description="Lifecycle constraints: 'To Do', 'In Progress', or 'Done'")
    story_points: int = Field(..., gt=0, description="Agile effort score estimation matrix must be greater than 0")
    assignee: str


class Sprint(BaseModel):
    sprint_id: str
    name: str
    target_velocity: int = Field(..., gt=0, description="Commitment velocity marker target")
    tasks: List[Task] = []


# ==========================================
# 2. IN-MEMORY DATABASE ARCHITECTURE
# ==========================================
# Simulating a relational schema tracking sprint execution histories
sprint_db: Dict[str, Sprint] = {
    "SPRINT-2026-01": Sprint(
        sprint_id="SPRINT-2026-01",
        name="Q2 Cloud Data Ingestion Layer Optimization",
        target_velocity=30,
        tasks=[
            Task(task_id="TSK-101", title="Configure Thread-Safe Resource Lock Routing", status="Done", story_points=8,
                 assignee="Alex"),
            Task(task_id="TSK-102", title="Optimize Local Storage JSON Writing Pools", status="Done", story_points=13,
                 assignee="Sam"),
            Task(task_id="TSK-103", title="Refactor Concurrent Thread Pool Size Allocation", status="In Progress",
                 story_points=5, assignee="Alex"),
            Task(task_id="TSK-104", title="Draft Architectural OpenAPI System Schemas", status="To Do", story_points=3,
                 assignee="Taylor")
        ]
    )
}


# ==========================================
# 3. RESTFUL SERVICE HTTP ENDPOINTS
# ==========================================
@app.get("/", tags=["Root Core Monitoring"])
def read_root():
    """System heartbeat verification handshake checking."""
    return {"status": "Online", "service": "Agile Analytics Engine Node"}


@app.get("/sprints/{sprint_id}/analytics", tags=["Data Aggregation Analytics"])
def get_sprint_analytics(sprint_id: str):
    """
    Business Logic Processing Core: Collects distributed active task attributes,
    calculates velocity ratios, and automatically identifies team delivery risk factors.
    """
    if sprint_id not in sprint_db:
        raise HTTPException(
            status_code=404,
            detail=f"Sprint data tracking matrix record context '{sprint_id}' not found."
        )

    sprint = sprint_db[sprint_id]

    completed_points = 0
    total_points = 0
    in_progress_bottlenecks = 0
    resource_allocation_matrix: Dict[str, int] = {}

    # Process sequential analytics data structures
    for task in sprint.tasks:
        total_points += task.story_points

        # Calculate workload distribution patterns across team engineering blocks
        resource_allocation_matrix[task.assignee] = resource_allocation_matrix.get(task.assignee, 0) + task.story_points

        if task.status == "Done":
            completed_points += task.story_points
        elif task.status == "In Progress":
            in_progress_bottlenecks += 1

    # Apply algorithmic validation calculations
    velocity_index = (completed_points / sprint.target_velocity) * 100
    completion_ratio = (completed_points / total_points) * 100 if total_points > 0 else 0

    # Flags system delivery vulnerabilities automatically based on bottleneck bounds
    is_sprint_delivery_at_risk = in_progress_bottlenecks >= 3 or completion_ratio < 40.0

    return {
        "sprint_identity_records": {
            "id": sprint.sprint_id,
            "sprint_name": sprint.name,
            "velocity_target_commitment": sprint.target_velocity
        },
        "performance_metrics_aggregation": {
            "actual_velocity_delivered": completed_points,
            "velocity_achievement_index": f"{round(velocity_index, 2)}%",
            "completion_ratio": f"{round(completion_ratio, 2)}%"
        },
        "operational_risk_evaluation": {
            "total_tracked_tasks": len(sprint.tasks),
            "unresolved_bottleneck_count": in_progress_bottlenecks,
            "operational_delivery_compromised": is_sprint_delivery_at_risk
        },
        "workload_distribution_matrix": resource_allocation_matrix
    }


@app.post("/sprints/{sprint_id}/tasks", tags=["Project Registry Management"], status_code=201)
def add_task_to_sprint(sprint_id: str, task: Task):
    """Appends data-validated task models directly into the tracking database matrix."""
    if sprint_id not in sprint_db:
        raise HTTPException(status_code=404, detail="Target sprint tracking database entry missing.")

    # Protect against record primary key identifier duplication collisions
    for existing_task in sprint_db[sprint_id].tasks:
        if existing_task.task_id == task.task_id:
            raise HTTPException(
                status_code=400,
                detail=f"Task identifier resource key '{task.task_id}' is allocation locked."
            )

    sprint_db[sprint_id].tasks.append(task)
    return {"message": "Task structural entity appended cleanly.", "task_id": task.task_id}


# Local sandboxed uvicorn runtime execution trigger hook
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_dashboard:app", host="127.0.0.1", port=8000, reload=True)