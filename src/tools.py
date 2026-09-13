"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Đề tài: Trợ lý đặt lịch tập Gym
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu thông tin hội viên & lịch tập Gym
    {
        "name": "gym_query",
        "description": "Tra cứu thông tin hội viên, gói tập, lịch tập và tình trạng phòng tập Gym bằng mã hội viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {
                    "type": "string",
                    "description": "Mã hội viên cần tra cứu (ví dụ: 'GYM12345')"
                }
            },
            "required": ["member_id"]
        }
    },

    # Tool 2: Đặt lịch tập Gym với PT (Hoàn thành TODO 1.2)
    {
        "name": "book_session",
        "description": "Đặt lịch buổi tập Gym với huấn luyện viên cá nhân (Personal Trainer - PT).",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {
                    "type": "string",
                    "description": "Mã hội viên cần đặt lịch tập (ví dụ: 'GYM12345')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian buổi tập (ví dụ: '18:00 15/09/2026')"
                },
                "trainer_name": {
                    "type": "string",
                    "description": "Tên huấn luyện viên cá nhân (PT) cần đặt lịch (ví dụ: 'PT Nguyễn Văn A')"
                }
            },
            "required": ["member_id", "datetime_str", "trainer_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "GYM12345": {
        "full_name": "Mai Hoàng Anh",
        "membership": "Gói Premium 12 tháng",
        "email": "hoanganh@gmail.com",
        "status": "Đang hoạt động",
        "expiry_date": "31/12/2026",
        "trainer": "PT Nguyễn Văn A",
        "sessions_remaining": 18
    },
    "GYM67890": {
        "full_name": "Trần Thị Bình",
        "membership": "Gói Basic 6 tháng",
        "email": "binh.tt@gmail.com",
        "status": "Đang hoạt động",
        "expiry_date": "28/02/2027",
        "trainer": "PT Trần Thị B",
        "sessions_remaining": 10
    }
}


def execute_gym_query(member_id: str) -> str:
    """Thực thi tra cứu thông tin hội viên Gym theo mã hội viên"""
    member = MOCK_DATABASE.get(member_id.strip().upper())
    if member:
        return json.dumps({
            "status": "SUCCESS",
            "member_id": member_id,
            "data": member
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy hội viên có mã '{member_id}'. Vui lòng kiểm tra lại mã hội viên."
        }, ensure_ascii=False)


def execute_book_session(member_id: str, datetime_str: str, trainer_name: str = "PT Nguyễn Văn A") -> str:
    """Thực thi đặt lịch buổi tập Gym với PT"""
    member = MOCK_DATABASE.get(member_id.strip().upper())
    if not member:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy hội viên có mã '{member_id}'. Không thể đặt lịch."
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{member_id}-{datetime_str.replace(' ', '').replace('/', '')}",
        "member_id": member_id,
        "member_name": member["full_name"],
        "datetime": datetime_str,
        "trainer": trainer_name,
        "message": f"Đặt lịch tập thành công cho hội viên {member['full_name']} ({member_id}) với {trainer_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "gym_query": execute_gym_query,
    "book_session": execute_book_session
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
