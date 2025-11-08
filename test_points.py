# test_points.py
from outer_polygon import find_outer_polygon, Point
import matplotlib.pyplot as plt

def plot_two_polygons(left_points, right_points, right_outer, offset):
    """
    并排绘制：
    - 左侧：原始点集（不计算外轮廓，逆时针顺序）
    - 右侧：平移后的点集 + 重新计算的外轮廓（逆时针）
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # === 左侧：原始点集（直接绘制，不计算外轮廓）===
    px1 = [p.X for p in left_points]
    py1 = [p.Y for p in left_points]
    px1_closed = px1 + [px1[0]]
    py1_closed = py1 + [py1[0]]

    ax1.scatter(px1, py1, c='blue', s=30, label='All Points (CCW)')
    ax1.plot(px1_closed, py1_closed, 'b--', linewidth=1, alpha=0.7, label='Point Order (CCW)')
    ax1.fill(px1_closed, py1_closed, alpha=0.1, color='lightblue')
    ax1.set_title("Original Points (CCW Order, No Outer)")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.legend()
    # ax1.grid(True)  # 去掉网格
    ax1.axis('equal')

    # === 右侧：平移 + 重新计算外轮廓（逆时针）===
    px2 = [p.X for p in right_points]
    py2 = [p.Y for p in right_points]
    ox2 = [p.X for p in right_outer] + [right_outer[0].X]
    oy2 = [p.Y for p in right_outer] + [right_outer[0].Y]

    ax2.scatter(px2, py2, c='gray', s=20, alpha=0.6, label='Translated Points')
    ax2.plot(ox2, oy2, 'r-', linewidth=2, label='Outer Polygon (CCW)')
    ax2.fill(ox2, oy2, alpha=0.2, color='red')
    ax2.set_title(f"Translated +{offset:.1f} → Outer (CCW)")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.legend()
    # ax2.grid(True)  # 去掉网格
    ax2.axis('equal')

    plt.suptitle("Left: Original Points (CCW) | Right: Translated + Outer Polygon (CCW)", fontsize=16)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 原始点集（逆时针顺序）
    points = [
        Point(1, 1), Point(2, 2), Point(3, 1), Point(4, 1),
        Point(10, 1), Point(10, 4), Point(12, 4), Point(12, 1),
        Point(17, 3), Point(17, 10), Point(16, 10), Point(16, 6),
        Point(14, 5), Point(14, 10), Point(13, 10), Point(13, 12),
        Point(12, 11), Point(12, 13), Point(11, 13), Point(11, 15),
        Point(9, 15), Point(9, 11), Point(8, 11), Point(8, 16),
        Point(7, 16), Point(7, 13), Point(6, 13), Point(6, 17),
        Point(5, 17), Point(5, 19), Point(4, 19), Point(1, 19),
        Point(1, 17), Point(2, 17), Point(2, 15), Point(1, 15),
        Point(1, 13), Point(3, 13), Point(3, 10), Point(1, 10),
        Point(1, 1)
    ]

    # 步骤 1：计算左侧最大 x（用于自动偏移）
    max_x_left = max(p.X for p in points)
    offset_x = max_x_left + 5  # 间距 5

    # 步骤 2：平移点集
    right_points = [Point(p.X + offset_x, p.Y) for p in points]

    # 步骤 3：对平移后的点集计算外轮廓（算法保证逆时针）
    right_outer = find_outer_polygon(right_points)

    # 绘图
    plot_two_polygons(points, right_points, right_outer, offset_x)