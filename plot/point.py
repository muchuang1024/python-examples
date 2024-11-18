import matplotlib.pyplot as plt

# 每个时间点的预约时间数据
time_strings = [
    "09:05",
    "09:16",
    "09:28",
    "09:36",
    "09:41",
    "09:45",
    "09:49",
    "09:52",
    "09:59",
    "09:00",
    "09:10",
    "09:21",
    "09:31",
    "09:39",
    "09:46",
    "09:50",
    "09:56",
    "09:07",
    "09:15",
    "09:26",
]
appointment_times = [
    "10:13",
    "10:32",
    "10:46",
    "10:54",
    "10:59",
    "10:03",
    "10:07",
    "10:10",
    "10:17",
    "10:00",
    "10:08",
    "10:19",
    "10:29",
    "10:37",
    "10:44",
    "10:48",
    "10:54",
    "10:05",
    "10:13",
    "10:24",
]


# 将时间字符串转换为分钟数
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes


# 绘制散点图
plt.figure(figsize=(10, 6))
plt.scatter(
    [time_to_minutes(time_str) for time_str in time_strings],
    [time_to_minutes(time_str) for time_str in appointment_times],
)
plt.xlabel("Time")
plt.ylabel("Appointment Time")
plt.title("Appointment Time vs. Time")
plt.xticks(range(540, 661, 30), ["09:00", "09:30", "10:00", "10:30", "11:00"])
plt.yticks(
    range(600, 661, 5),
    [
        "10:00",
        "10:05",
        "10:10",
        "10:15",
        "10:20",
        "10:25",
        "10:30",
        "10:35",
        "10:40",
        "10:45",
        "10:50",
        "10:55",
        "11:00",
    ],
)
plt.grid(True)
plt.show()
