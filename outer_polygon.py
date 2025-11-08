# outer_polygon.py
from typing import List, Tuple
from dataclasses import dataclass
import math

@dataclass
class Point:
    X: float
    Y: float

    def __eq__(self, other):
        return math.isclose(self.X, other.X) and math.isclose(self.Y, other.Y)

    def __hash__(self):
        return hash((self.X, self.Y))


class GeometryUtil:
    @staticmethod
    def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


# 模拟 C# List.GetRange(start, length)
def get_range(lst: List, start: int, length: int) -> List:
    """
    模拟 C# List.GetRange(start, length)
    - start >= len(lst) → 返回 []
    - length < 0 → 抛 ValueError（C# 行为）
    - start + length > len(lst) → 截断到末尾
    """
    if length < 0:
        raise ValueError("Length cannot be negative.")
    if start < 0:
        start = 0
    if start >= len(lst):
        return []
    end = start + length
    if end > len(lst):
        end = len(lst)
    return lst[start:end]


def find_outer_polygon(points: List[Point]) -> List[Point]:
    # Get the max x, max y, min x, min y
    minX = min(p.X for p in points)
    maxX = max(p.X for p in points)
    minY = min(p.Y for p in points)
    maxY = max(p.Y for p in points)

    # Initialize the four extreme vertices
    minYmaxX = Point(maxX, minY)
    maxYmaxX = Point(maxX, maxY)
    minYminX = Point(minX, minY)
    maxYminX = Point(minX, maxY)

    # Calculate the distance of each point to the four vertices
    distance_dict = []
    for p in points:
        dists = (
            GeometryUtil.calculate_distance((minYmaxX.X, minYmaxX.Y), (p.X, p.Y)),
            GeometryUtil.calculate_distance((maxYmaxX.X, maxYmaxX.Y), (p.X, p.Y)),
            GeometryUtil.calculate_distance((minYminX.X, minYminX.Y), (p.X, p.Y)),
            GeometryUtil.calculate_distance((maxYminX.X, maxYminX.Y), (p.X, p.Y)),
        )
        distance_dict.append({p: dists})

    # Find the point with the minimum distance to each vertex
    point1_distance = None
    point2_distance = None
    point3_distance = None
    point4_distance = None

    for item in distance_dict:
        for k, v in item.items():
            if point1_distance is None or v[0] < point1_distance:
                point1_distance = v[0]
                minYmaxX = k

            if point2_distance is None or v[1] < point2_distance:
                point2_distance = v[1]
                maxYmaxX = k

            if point3_distance is None or v[2] < point3_distance:
                point3_distance = v[2]
                minYminX = k

            if point4_distance is None or v[3] < point4_distance:
                point4_distance = v[3]
                maxYminX = k

    result = []

    # Get the index of the minimum y, minimum x point
    min_y_min_x_idx = points.index(minYminX)

    # Replace the value of the top left highest point
    points[points.index(maxYminX)] = Point(minX, maxY)
    maxYminX = Point(minX, maxY)

    # Rotate the points so that the minimum y, minimum x point is the starting point
    points = points[min_y_min_x_idx:] + points[:min_y_min_x_idx]
    min_y_min_x_idx = 0
    minYmaxX_idx = points.index(minYmaxX)
    maxYmaxX_idx = points.index(maxYmaxX)
    maxYminX_idx = points.index(maxYminX)

    # Process the first edge
    points_1 = get_range(points, min_y_min_x_idx, minYmaxX_idx - min_y_min_x_idx + 1)
    if points_1 and points_1[-1].Y > points_1[0].Y:
        points_1[-1] = Point(points_1[-1].X, minY)

    result = GetPoints1(points_1[0], points_1, result)

    # Process the second edge
    points_2 = get_range(points, minYmaxX_idx, maxYmaxX_idx - minYmaxX_idx + 1)
    if points_2:
        points_2[0] = points_1[-1]
    result = GetPoints2(points_2[0], points_2, result)

    # Process the third edge
    points_3 = get_range(points, maxYmaxX_idx, maxYminX_idx - maxYmaxX_idx + 1)
    if points_3 and maxY > points_3[0].Y:
        CovexIdx = 0
        for i in range(1, len(points_3)):
            if points_3[i].Y == maxY:
                CovexIdx = points.index(points_3[i])
                break

        points_3_up = get_range(points, maxYmaxX_idx, CovexIdx - maxYmaxX_idx + 1)
        result = GetPoints2(points_3_up[0], points_3_up, result)
        points_3_down = get_range(points, CovexIdx, maxYminX_idx - CovexIdx + 1)
        result = GetPoints3(points_3_down[0], points_3_down, result)
    else:
        result = GetPoints3(points_3[0], points_3, result)

    # Process the fourth edge
    points_4 = get_range(points, maxYminX_idx, len(points) - maxYminX_idx)
    points_4.extend(points[:min_y_min_x_idx + 1])
    if points_4 and minX < points_4[0].X:
        CovexIdx = 0
        for i in range(1, len(points_4)):
            if points_4[i].X == minX:
                CovexIdx = points.index(points_4[i])
                break

        points_4_up = get_range(points, maxYminX_idx, CovexIdx - maxYminX_idx + 1)
        result = GetPoints3(points_4_up[0], points_4_up, result)
        points_4_down = get_range(points, CovexIdx, len(points) - CovexIdx)
        result = GetPoints4(points_4_down[0], points_4_down, result)
    else:
        result = GetPoints4(points_4[0], points_4, result)

    return result


def GetPoints1(point, points, result):
    pp = point
    if len(points) >= 2:
        result.append(point)

        convexPoints = [p for p in points if p.Y <= pp.Y and p.X > pp.X]

        if len(convexPoints) > 0:
            convexPointY = min(convexPoints, key=lambda p: p.Y)
            convexPoint = max([p for p in convexPoints if p.Y == convexPointY.Y], key=lambda p: p.X)

            if convexPoint.Y < pp.Y:
                result.remove(point)

            result.append(Point(pp.X, convexPoint.Y))

            pointIndex = points.index(convexPoint)

            if pointIndex < len(points) - 1:
                point = points[pointIndex]
                points = get_range(points, pointIndex, len(points) - pointIndex)
                return GetPoints1(point, points, result)

            if pointIndex == len(points) - 1:
                return result
        else:
            pointIndex = points.index(point)
            if pointIndex < len(points) - 1:
                point = points[pointIndex + 1]
                points = get_range(points, pointIndex + 1, len(points) - pointIndex - 1)
                return GetPoints1(point, points, result)
            else:
                return result
    else:
        return result

    return result


def GetPoints2(point, points, result):
    pp = point

    if len(points) >= 2:
        result.append(point)

        convexPoints = [p for p in points if p.X >= pp.X and p.Y > pp.Y]

        if len(convexPoints) > 0:
            convexPointX = max(convexPoints, key=lambda p: p.X)
            convexPoint = max([p for p in convexPoints if p.X == convexPointX.X], key=lambda p: p.Y)

            if convexPoint.X > pp.X:
                result.remove(point)

            result.append(Point(convexPoint.X, pp.Y))

            pointIndex = points.index(convexPoint)

            if pointIndex < len(points) - 1:
                point = points[pointIndex]
                points = get_range(points, pointIndex, len(points) - pointIndex)
                return GetPoints2(point, points, result)

            if pointIndex == len(points) - 1:
                return result
        else:
            points = [Point(p.X, point.Y) if p.X < point.X and p.Y < point.Y else p for p in points]
            pointIndex = points.index(point)
            if pointIndex < len(points) - 1:
                point = points[pointIndex + 1]
                points = get_range(points, pointIndex + 1, len(points) - pointIndex - 1)
                return GetPoints2(point, points, result)
            else:
                return result
    else:
        return result

    return result


def GetPoints3(point, points, result):
    pp = point

    if len(points) >= 2:
        result.append(point)

        convexPoints = [p for p in points if p.Y > pp.Y and p.X <= pp.X]

        if len(convexPoints) > 0:
            convexPointY = max(convexPoints, key=lambda p: p.Y)
            convexPoint = min([p for p in convexPoints if p.Y == convexPointY.Y], key=lambda p: p.X)

            if convexPoint.Y > pp.Y:
                result.remove(point)

            result.append(Point(pp.X, convexPoint.Y))

            pointIndex = points.index(convexPoint)

            if pointIndex < len(points) - 1:
                point = points[pointIndex]
                points = get_range(points, pointIndex, len(points) - pointIndex)
                return GetPoints3(point, points, result)

            if pointIndex == len(points) - 1:
                return result
        else:
            pointIndex = points.index(point)
            if pointIndex < len(points) - 1:
                point = points[pointIndex + 1]
                points = get_range(points, pointIndex + 1, len(points) - pointIndex - 1)
                return GetPoints3(point, points, result)
            else:
                return result
    else:
        return result

    return result


def GetPoints4(point, points, result):
    pp = point

    if len(points) >= 2:
        result.append(point)

        convexPoints = [p for p in points if p.X <= pp.X and p.Y < pp.Y]

        if len(convexPoints) > 0:
            convexPointX = min(convexPoints, key=lambda p: p.X)
            convexPoint = min([p for p in convexPoints if p.X == convexPointX.X], key=lambda p: p.Y)

            result.append(Point(pp.X, convexPoint.Y))

            pointIndex = points.index(convexPoint)

            if pointIndex < len(points) - 1:
                point = points[pointIndex]
                points = get_range(points, pointIndex, len(points) - pointIndex)
                return GetPoints4(point, points, result)

            if pointIndex == len(points) - 1:
                return result
        else:
            pointIndex = points.index(point)
            if pointIndex < len(points) - 1:
                point = points[pointIndex + 1]
                points = get_range(points, pointIndex + 1, len(points) - pointIndex - 1)
                return GetPoints4(point, points, result)
            else:
                return result
    else:
        return result

    return result